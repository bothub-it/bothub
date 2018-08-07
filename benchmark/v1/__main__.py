import argparse
import traceback

from app import bothub
from app import wit
from app.bothub import save_on_bothub, store_result, analyze_text, train, create_new_repository, delete_repository, write_csv_file
from app.wit import read_wit_and_push_bothub
from app.utils import load_json_file#,percentage

parser = argparse.ArgumentParser(description='Train and Test the accuracy from Bothub')

sub_tasks = parser.add_subparsers(title='Tasks')


def fill_bothub(args):
    expressions = load_json_file(args.filename)
    repository_data = create_new_repository(args)
    print('Uploading examples...')
    if args.file_source != 'wit':
        for n, expression in enumerate(expressions['data']):
            entities = []
            if (len(expression['entities']) > 0):
                entities = expression['entities']
            try:
                save_on_bothub(repository_data[0], expression['text'], entities, expression['intent'])
            except KeyError:
                traceback.print_exc()
                print('Skipping expression {} due to an error'.format(expression))
    else:
        for expression in expressions['data']:
            entities = []
            if (len(read_wit_and_push_bothub(expression)[1])):
                entities = read_wit_and_push_bothub(expression)[1]
            save_on_bothub(repository_data[0],read_wit_and_push_bothub(expression)[0],entities,read_wit_and_push_bothub(expression)[2])

    train_repository(args)
    print('Generating report...')
    predict(args)
    delete_repository(args.ownernick, repository_data[1])


def decode_expressions_from_wit(args):
    expressions = load_json_file(args.filename)
    for expression in expressions['data']:
        read_wit_and_push_bothub(expression)


task_decode_wit = sub_tasks.add_parser('decode_wit', help='Reads a exported json from Wit')
task_decode_wit.add_argument('--filename', help='expressions.json')
task_decode_wit.set_defaults(func=decode_expressions_from_wit)


task_fill_bothub = sub_tasks.add_parser('fill_bothub', help='Insert data from a source to Bothub')
task_fill_bothub.add_argument('--repository', help='repository uuid destination on bothub')
task_fill_bothub.add_argument('--ownernick', help='Owner nickname')
task_fill_bothub.add_argument('--file_source', help='source from the file')
task_fill_bothub.add_argument('--slug', help='Repository slug')
task_fill_bothub.add_argument('--lang', help='language of the bot on Bothub')
task_fill_bothub.add_argument('--filename', help='name of the file that contains the phrases to be trained')
task_fill_bothub.add_argument('--testfilename', help='name of the file that contains the phrases to be tested')
task_fill_bothub.set_defaults(func=fill_bothub)


def predict(args):
    treated_predicts = []
    phrases_count = 0
    sum_bothub_hits = 0
    sum_bothub_fails = 0
    expressions = load_json_file(args.testfilename)
    for expression in expressions['data']:
        phrases_count += 1
        try:
                bothub_result = bothub.analyze_text(expression['value'], args.lang, args.ownernick, args.slug)
                treated_predicts.append(store_result(expression,bothub_result))
                if bothub_result['answer']['intent']['name'] == expression['intent']:
                    sum_bothub_hits += 1
                else:
                    sum_bothub_fails += 1
        except KeyError:
            traceback.print_exc()
            print('Skipping expression {} due to an error'.format(expression))
    # bothub_accuracy = percentage(sum_bothub_hits, count)
    # bothub_confidence_avg = sum_bothub_confidence/count
    write_csv_file(treated_predicts,'Analized phrases: {0}\nCorrect predictions: {1}\nWrong predictions: {2}'.format(phrases_count,sum_bothub_hits,sum_bothub_fails))
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
