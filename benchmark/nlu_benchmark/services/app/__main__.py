import argparse
import traceback

from app import bothub
from app.bothub import save_on_bothub, analyze, analyze_text, train, create_new_repository, delete_repository
from app.utils import load_json_file#,percentage

parser = argparse.ArgumentParser(description='Train and Test the accuracy from Bothub')

sub_tasks = parser.add_subparsers(title='Tasks')


def fill_bothub(args):
    expressions = load_json_file(args.filename)
    repository_data = create_new_repository(args)
    for n, expression in enumerate(expressions['data']):
        entities = []
        if (len(expression['entities']) > 0):
            entities = expression['entities']
        try:
            save_on_bothub(repository_data[0], expression['text'], entities, expression['intent'])
        except KeyError:
            traceback.print_exc()
            print('Skipping expression {} due to an error'.format(expression))
    
    train_repository(args)
    predict(args)
    delete_repository(args.ownernick, repository_data[1])

# Add another argument that stores a description of the test
task_fill_bothub = sub_tasks.add_parser('fill_bothub', help='Insert data from a source to Bothub')
task_fill_bothub.add_argument('--repository', help='repository uuid destination on bothub')
task_fill_bothub.add_argument('--ownernick', help='Owner nickname')
task_fill_bothub.add_argument('--slug', help='Repository slug')
task_fill_bothub.add_argument('--lang', help='language of the bot on Bothub')
# task_fill_bothub.add_argument('--source', help='path to the source file, e.g. intents.json')
task_fill_bothub.add_argument('--filename', help='name of the file that contains the phrases to be trained')
task_fill_bothub.add_argument('--testfilename', help='name of the file that contains the phrases to be tested')
task_fill_bothub.set_defaults(func=fill_bothub)


def predict(args):
    phrases_count = 0
    sum_bothub_hits = 0
    sum_bothub_fails = 0
    expressions = load_json_file(args.testfilename)
    for expression in expressions['data']:
        phrases_count += 1
        try:
                bothub_result = bothub.analyze_text(expression['value'], args.lang, args.ownernick, args.slug)#.analyze(expression['value'], args.lang)
                # print(bothub_result['answer']['intent']['name'])
                if bothub_result['answer']['intent']['name'] == expression['intent']:
                    sum_bothub_hits += 1
                    print(expression['value']+' '+expression['intent']+' - OK') #+bothub_result['answer']['intent']['confidence']
                else:
                    sum_bothub_fails += 1
                    print(expression['value']+' '+expression['intent']+' - FAILURE')
        except KeyError:
            traceback.print_exc()
            print('Skipping expression {} due to an error'.format(expression))

    print('============================ RESULT ================================')
    # bothub_accuracy = percentage(sum_bothub_hits, count)
    # bothub_confidence_avg = sum_bothub_confidence/count

    print('Bothub:')
    print('Analized phrases: {}'.format(phrases_count))
    print('Correct predictions: {}'.format(sum_bothub_hits))
    print('Wrong predictions: {}'.format(sum_bothub_fails))
    # print('Final Accuracy: {}'.format(bothub_accuracy))
    # print('Average Confidence: {}%'.format(bothub_confidence_avg))

def open_repository(args):
    create_new_repository(args)

task_predict = sub_tasks.add_parser('open_repository', help='Predict from Bothub and check accuracy')
task_predict.set_defaults(func=open_repository)

def remove_repository(args):
    delete_repository(args.ownernick, args.slug)

task_train = sub_tasks.add_parser('remove_repository', help='Train all data uploaded to Bothub')
task_train.add_argument('--slug', help='slog fromt he repository')
task_train.add_argument('--ownernick', help='Owner nickname')
task_train.set_defaults(func=remove_repository)



task_predict = sub_tasks.add_parser('predict', help='Predict from Bothub and check accuracy')
# task_predict.add_argument('--authorization-bothub', help='authorization token from dataset on Bothub')
# task_predict.add_argument('--source', help='path to the source file, e.g. intents.json')
task_predict.add_argument('--testfilename', help='name of the source file')
task_predict.add_argument('--intent', help='name of the entity that represents the intents')
task_predict.add_argument('--lang', help='language of the bot on Bothub')
task_predict.set_defaults(func=predict)

def train_repository(args):
    train(args.ownernick, args.slug)


task_train = sub_tasks.add_parser('train_repository', help='Train all data uploaded to Bothub')
task_train.add_argument('--slug', help='slog fromt he repository')
task_train.add_argument('--ownernick', help='Owner nickname')
task_train.set_defaults(func=train_repository)

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
