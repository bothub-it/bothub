import plac
import yaml
import json
import requests
import zipfile
import unicodedata

from tqdm import tqdm

from . import logger
from ..services.bothub import Bothub
from ..services.wit import Wit

@plac.annotations(
    data_file_path=plac.Annotation(),
    data_file_type=plac.Annotation(kind='option', choices=['yaml', 'json']),
    bothub_user_token=plac.Annotation(kind='option'),
    type_tests=plac.Annotation(kind='flag', abbrev='T'))
def run(data_file_path, data_file_type='yaml', bothub_user_token=None,
        type_tests=False):
    try:
        data_file = open(data_file_path, 'r')
    except Exception as e:
        logger.error(f'Can\'t open the data file "{data_file_path}"')
        raise e

    try:
        if data_file_type == 'yaml':
            data = yaml.load(data_file)
        elif data_file_type == 'json':
            data = json.load(data_file)
    except Exception as e:
        raise e

    logger.debug(f'data loaded to run benchmark {data}')

    bothub_global_config = Bothub.get_current_global_config()

    bothub_user_token = bothub_user_token or bothub_global_config.get('user_token')
    assert bothub_user_token
    logger.debug(f'using {bothub_user_token} bothub user token')

    logger.info('Starting Bothub benchmark...')
    bothub = Bothub(user_token=bothub_user_token)
    wit = Wit()

    ## Create a temporary repository

    create_repository_response = bothub.create_temporary_repository(data.get('language'))

    try:
        create_repository_response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.error('Bothub temporary repository not created')
        logger.debug(create_repository_response.text)
        raise e

    temporary_repository = create_repository_response.json()
    logger.info(f'Bothub temporary repository created "{temporary_repository.get("name")}"')


    try:
        ## Train
        train = data.get('train')
        if 'filetype' in train[2] and train[4].get('filetype') != 'zip':
            total_train = len(train)
            logger.info(f'{total_train} examples to train in Bothub')
            with tqdm(total=total_train, unit='examples') as pbar:
                for example in train:
                    example_submit_response = bothub.submit_example(temporary_repository.get('uuid'), example, data.get('language'))
                    logger.debug(f'example trained {example_submit_response.text}')
                    example_submit_response.raise_for_status()
                    pbar.update(1)
            logger.info('Examples submitted!')
        else:
            with zipfile.ZipFile(data.get('train')[0].get('filepath'),'r') as training_file:
                with training_file.open('ProjetoJá/expressions.json') as json_file:
                    training_data = json.loads(json_file.read().decode('utf-8'))
            for expression in training_data['data']:
                text = expression['text']
                wit_entities = []
                if 'entities' in expression:
                    wit_entities = expression['entities']
                filtered_entities = []
                intent = ''
                for entity in wit_entities:
                    if entity['entity'] == 'intent':
                        intent = entity['value'].strip('\"').lower()
                    else:
                        new_entity = {}
                        new_entity['entity'] = ''.join(c for c in unicodedata.normalize('NFD', entity['value'].strip('\"').replace(' ','_').lower()) if unicodedata.category(c) != 'Mn')
                        
                        if 'start' in entity:
                            new_entity['start'] = entity['start']
                        else:
                            new_entity['start'] = 0
                        
                        if 'end' in entity:
                            new_entity['end'] = entity['end']
                        else:
                            new_entity['end'] = len(text)
                        
                        new_entity['label'] = entity['entity']

                        if bool(new_entity):
                            filtered_entities.append(new_entity)

                if len(filtered_entities) > 0 or intent != '':
                    example_submit_response = bothub.submit_from_wit_format(temporary_repository.get('uuid'),[text,filtered_entities,intent])
                    logger.debug(f'example trained {example_submit_response.text}')
                    example_submit_response.raise_for_status()
            logger.info('Examples submitted!')
                
        logger.info('Training...')
        train_response = bothub.train(temporary_repository.get('owner__nickname'), temporary_repository.get('slug'))
        logger.debug(f'repository train response {train_response.text}')
        train_response.raise_for_status()
        logger.info('Repository trained')

        ## Test

        test_bothub_result = []
        test_wit_result = []
        result_intent_test = ''
        def analyze_wrapper(text, expected={}):

            analyze_response = bothub.analyze(
                temporary_repository.get('owner__nickname'),
                temporary_repository.get('slug'),
                text,
                data.get('language'))
            logger.debug(f'analyze response {analyze_response.text}')
            analyze_response.raise_for_status()
            analyze = analyze_response.json()
            analyze_intent = analyze.get('intent')
            result_intent_test = 'FALSE'
            if expected[0].get('intent') == analyze_intent.get('name'):
                result_intent_test = 'OK'             
            logger.info('Bothub return:')
            logger.info(f' - intent: {analyze_intent.get("name", "[not detected]")} ' +
                        f'({int(analyze_intent.get("confidence", 0) * 100)}%)')
            test_bothub_result.append({
                'text': text,
                'intent': analyze_intent,
                'entities': analyze.get('entities'),
                'expected': expected,
                'result': result_intent_test
            })

            analyze_wit_response = wit.analyze(text,data.get('train')[3],data.get('train')[2].get('wit_token'))
            entities = analyze_wit_response.json().get('entities')
            
            # wit_entities_percentage:int = 0
            # wit_entity_result = ''
            # entity_matches: int = 0
            # known_entities_test = []
            # entities_from_wit = []
            # intent_result = ''
            # intent_confidence_result: int = 0
            # detected_entities_wit = '|'
            # intent_test_result = 'FALSE'
            
            # for entity in entities:
            #     if entity != 'intent':
            #         for item in entities.get(entity):
            #             entities_from_wit.append(entity.lower())
            #             detected_entities_wit += '{0}=>{1}|'.format(item.get('value'), entity)
            # for item in expected:
            #     if 'entities' in item:
            #         for entity in item.get('entities'):
            #             known_entities_test.append(entity.get('entity').lower())
            # for item in entities_from_wit:
            #     for expected_item in known_entities_test:
            #         if item == expected_item:
            #             entity_matches += 1
            #             break
            # if len(entities_from_wit) == len(known_entities_test) == entity_matches:
            #     wit_entity_result = 'OK'
            #     wit_entities_percentage = 100
            # elif (len(entities_from_wit) != entity_matches or entity_matches != len(known_entities_test)) and entity_matches > 0:
            #     wit_entities_percentage = (entity_matches/len(known_entities_test))*100
            #     wit_entity_result = 'PARCIAL'
            # else:
            #     wit_entities_percentage = 0
            #     wit_entity_result = 'FAILURE'

            # if 'intent' in entities:
            #     intent_result = entities.get('intent')[0].get('value')
            #     intent_confidence_result = entities.get('intent')[0].get('confidence')
            #     if expected[0].get('intent') == intent_result:
            #         intent_test_result = 'OK'
            # test_wit_result.append({
            #     'text': text,
            #     'intent': intent_result,
            #     'confidence': intent_confidence_result,
            #     'expected':expected,
            #     'entities': detected_entities_wit,
            #     'result': intent_test_result,
            #     'entity_percentage': wit_entities_percentage,
            #     'entity_result': wit_entity_result
            # })
            # intent_result = ''

        if type_tests:
            logger.warning('Typing mode ON, press CTRL + C to exit')
            try:
                while True:
                    text = input('Type a text to test: ')
                    analyze_wrapper(text)
            except KeyboardInterrupt as e:
                logger.info('Test finished!')
        else:
            for test in data.get('tests'):
                analyze_wrapper(test.get('text'), test.get('expected'))

        logger.debug(f'test_bothub_result: {test_bothub_result}')
    except requests.exceptions.HTTPError as e:
        raise e
    except Exception as e:
        raise e
    finally:

        ## Write CSV file with test results

        logger.info(f'Writing CSV files...')
        csv_headers = "Phrases,Expected intents,Bothub predicts,Confidence accuracy,Result by Intent,Detected entities,Expected entities,Result by Entity, Entity accuracy\n"
        expected_entities = ''
        with open('Bothub_output.csv', 'w') as csv_file:
            bothub_hits: int = 0
            bothub_failures: int = 0
            bothub_entities_count: int = 0
            known_entities_count: int = 0
            matched_entities: int = 0
            entities_percentage: int = 0
            entity_result = ''
            csv_file.write(csv_headers)
            for example in test_bothub_result:
                entities = ''
                expected_entities = '|'
                if len(example.get('expected')) > 1:
                    for entity in example.get('expected')[1].get('entities'):
                        known_entities_count += 1
                        expected_entities += '{0}=>{1}|'.format(entity.get('value'), entity.get('entity'))
                print(example)    
                if ('entities' in example) and (len(example.get('entities')) > 0):
                    entities = '|'
                    for entity in example.get('entities'):
                        bothub_entities_count += 1
                        if (entity == 'other') and len(example.get('entities').get('other')) > 0:
                            for entity in example.get('entities').get('other'):
                                entities += '{0}=>{1}|'.format(entity.get('value'), entity.get('entity'))
                        if len(example.get('expected')) > 1:
                            for known_entity in example.get('expected')[1].get('entities'):
                                for entity_without_label in example.get('entities').get('other'):
                                    if entity_without_label.get('entity').lower() == known_entity.get('entity').lower():
                                        matched_entities += 1
                if example.get('result') == 'OK':
                    bothub_hits += 1
                else:
                    bothub_failures += 1
                if bothub_entities_count == known_entities_count == matched_entities:
                    entity_result = 'OK'
                    entities_percentage = 100
                elif bothub_entities_count != known_entities_count and matched_entities > 0:
                    entities_percentage = (bothub_entities_count/known_entities_count)*100
                    entity_result = 'PARCIAL'
                else:
                    entities_percentage = 0
                    entity_result = 'FAILURE'

                csv_file.write('{0},{1},{2},{3}%,{4},{5},{6},{7},{8}%'.format(example.get('text'),example.get('expected')[0].get('intent'),example.get('intent').get('name'),int(example.get('intent').get('confidence')*100),example.get('result'),entities,expected_entities,entity_result,entities_percentage))
                csv_file.write('\n')
                bothub_entities_count: int = 0
                known_entities_count: int = 0
                matched_entities: int = 0
                entities_percentage: int = 0
                entity_result = ''                                
            csv_file.write('\n' + 'Analized phrases: {0}\nSuccess average: {1}%\nWrong predictions: {2}'.format(len(test_bothub_result), bothub_hits,bothub_failures))
        logger.info(f'Bothub_output.csv saved!')

        # csv_headers = "Phrases,Expected intents,Wit predicts,Confidence accuracy,Result by Intent,Detected entities,Expected entities,Result by Entity, Entity accuracy\n"
        # with open('Wit_output.csv','w') as csv_file:
        #     wit_hits: int = 0
        #     wit_failures: int = 0
        #     csv_file.write(csv_headers)
        #     for example in test_wit_result:
        #         expected_entities = '|'
        #         if len(example.get('expected')) > 1:
        #             for entity in example.get('expected')[1].get('entities'):
        #                 expected_entities += '{0}=>{1}|'.format(entity.get('value'), entity.get('entity'))
        #         if example.get('result') == 'OK':
        #             wit_hits += 1
        #         else:
        #             wit_failures += 1
        #         csv_file.write('{0},{1},{2},{3}%,{4},{5},{6},{7},{8}%'.format(example.get('text'),example.get('expected')[0].get('intent'),example.get('intent'),int(example.get('confidence')*100),example.get('result'),example.get('entities'),expected_entities,example.get('entity_result'),example.get('entity_percentage')))
        #         csv_file.write('\n')
        #     csv_file.write('\n' + 'Analized phrases: {0}\nSuccess average: {1}%\nWrong predictions: {2}'.format(len(test_wit_result), wit_hits,wit_failures))
        # logger.info(f'Wit_output.csv saved!')
        ## Delete a temporary repository

        # delete_repository_response = bothub.delete_repository(
        #     temporary_repository.get('owner__nickname'),
        #     temporary_repository.get('slug'))

        # try:
        #     delete_repository_response.raise_for_status()
        # except Exception as e:
        #     logger.warning('Bothub temporary repository not deleted, manually delete')
        #     logger.debug(delete_repository_response.text)

        logger.info(f'Bothub temporary repository deleted')

        bothub.delete_repository(temporary_repository.get('owner__nickname'),'577O11KN2BS06MXG')
        bothub.delete_repository(temporary_repository.get('owner__nickname'),'L6FLKN2GQHAJ0M80')
        bothub.delete_repository(temporary_repository.get('owner__nickname'),'DHIHOM1XEQ4BAM95')
        bothub.delete_repository(temporary_repository.get('owner__nickname'),'PEB90GJREPHJCL1U')
        bothub.delete_repository(temporary_repository.get('owner__nickname'),'GT4GFLO03CZHHSHF')
        bothub.delete_repository(temporary_repository.get('owner__nickname'),'28QTVA36R17TQJUA')
        bothub.delete_repository(temporary_repository.get('owner__nickname'),'14LR7RNRFH3JCBJB')
        bothub.delete_repository(temporary_repository.get('owner__nickname'),'JU5TMUUMRQM26F0D')
        bothub.delete_repository(temporary_repository.get('owner__nickname'),'UTIJPUJHV4H2VEJT')
        bothub.delete_repository(temporary_repository.get('owner__nickname'),'WA1JC2PP77EYXSWS')
        bothub.delete_repository(temporary_repository.get('owner__nickname'),'BDLOYC6SFI256GU0')
        bothub.delete_repository(temporary_repository.get('owner__nickname'),'HP1572M3AOP9D562')
        bothub.delete_repository(temporary_repository.get('owner__nickname'),'2JERLTQIZM14J2N9')
        bothub.delete_repository(temporary_repository.get('owner__nickname'),'7YWPENL495FBP5SO')
        bothub.delete_repository(temporary_repository.get('owner__nickname'),'DNFPW93RCWR4IF6L')
        bothub.delete_repository(temporary_repository.get('owner__nickname'),'QANTJ2C8W3948AA4')
        bothub.delete_repository(temporary_repository.get('owner__nickname'),'HHSUD0RXCH72P5RY')