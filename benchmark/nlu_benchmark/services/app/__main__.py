import argparse
import traceback

from app import bothub
from app.bothub import save_on_bothub, analyze, train
from app.utils import load_json_file#,percentage

parser = argparse.ArgumentParser(description='Train and Test the accuracy from Bothub')

sub_tasks = parser.add_subparsers(title='Tasks')


def fill_bothub(args):
    expressions = load_json_file(args.filename)
    
    for n, expression in enumerate(expressions['data']):
        try:
            entity = expression['entities'][0]
            entity_name = entity['entity']

            if entity_name == args.intent:
                save_on_bothub(args, expression['text'], entity['value'])
        except KeyError:
            traceback.print_exc()
            print('Skipping expression {} due to an error'.format(expression))

# Add another argument that stores a description of the test
task_fill_bothub = sub_tasks.add_parser('fill_bothub', help='Insert data from a source to Bothub')
task_fill_bothub.add_argument('--repository', help='repository uuid destination on bothub')
# task_fill_bothub.add_argument('--source', help='path to the source file, e.g. intents.json')
task_fill_bothub.add_argument('--intent', help='name of the entity that represents the intents')
task_fill_bothub.add_argument('--filename', help='name of the file that contains the phrases to be trained')
task_fill_bothub.add_argument('--testfilename', help='name of the file that contains the phrases to be tested')
task_fill_bothub.set_defaults(func=fill_bothub)


def predict(args):
    phrases_count = 0
    sum_bothub_hits = 0
    expressions = load_json_file(args.testfilename)
    for expression in expressions['data']:
        phrases_count += 1
        try:
                bothub_result = bothub.analyze(expression['value'], args.lang)
                if bothub_result['answer']['intent']['name'] == expression[args.intent]:
                    sum_bothub_hits += 1
                    print(expression['value']+' '+expression['intent']+' - OK') #+bothub_result['answer']['intent']['confidence']
        except KeyError:
            traceback.print_exc()
            print('Skipping expression {} due to an error'.format(expression))

    print('============================ RESULT ================================')
    # bothub_accuracy = percentage(sum_bothub_hits, count)
    # bothub_confidence_avg = sum_bothub_confidence/count

    print('Bothub:')
    print('Analized phrases: {}'.format(phrases_count))
    print('Correct predictions: {}'.format(sum_bothub_hits))
    # print('Final Accuracy: {}'.format(bothub_accuracy))
    # print('Average Confidence: {}%'.format(bothub_confidence_avg))


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
