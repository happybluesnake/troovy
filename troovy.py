'''

_|_|_|_|_|                                                      
    _|      _|  _|_|    _|_|      _|_|    _|      _|  _|    _|  
    _|      _|_|      _|    _|  _|    _|  _|      _|  _|    _|  
    _|      _|        _|    _|  _|    _|    _|  _|    _|    _|  
    _|      _|          _|_|      _|_|        _|        _|_|_|  
                                                            _|  
                                                        _|_|

'''
import argparse, random
from troovy_cfg import questions, answer_choices, correct_answer, success_messages, failure_messages

def no_silly_numbers(number):
    ''' Troovy can accept 1 argument, -a or --amount, the amount of questions to ask. This function verifies the argument is greater than 0. '''
    check = int(number)
    if check <= 0:
         raise argparse.ArgumentTypeError('Please enter a number greater than 0.')
    return check

parser = argparse.ArgumentParser(description='Troovy | The Groovy Woovy Trivia Game')
parser.add_argument('-a',
                    '--amount',
                    type=no_silly_numbers,
                    default=10,
                    help='The amount of Troovy questions to ask.')
args = parser.parse_args()

class troovyGame:

    def troovy(self):
        ''' Handles the main components of the program to make it completely functional. '''
        self.check_choices()
        print('Welcome to Troovy!\n')
        answer_choices_dict = {}
        abcd = [
            'A',
            'B',
            'C',
            'D'
        ]
        correct = 0
        total = 0
        for current_question in range(0, args.amount):
            question_index, question = random.choice(list(questions.items()))
            answer_choices_randomized_split = self.randomize_questions(question_index,
                                                                                                      question)
            print('{}. {}\n'.format((current_question + 1),
                                                question))
            for answer in range(65, 65 + len(answer_choices_randomized_split)):
                answer_char = chr(answer)
                answer_text = answer_choices_randomized_split[65 - answer].strip()
                answer_choices_dict.update(
                    {
                        answer_char:answer_text
                    })
                print('{} - {}'.format(answer_char,
                                                answer_text))
            selected_answer_ascii = self.verify_answer(abcd)
            selected_answer_text = answer_choices_randomized_split[65 - selected_answer_ascii].strip()
            print('You selected: {} - {}.'.format(chr(selected_answer_ascii),
                                                                  selected_answer_text))
            correct, total = self.check_answer(question_index,
                                                              selected_answer_text,
                                                              answer_choices_dict,
                                                              correct,
                                                              total)
        self.print_results(correct,
                                 total)
        
    def randomize_questions(self, question_index, question):
        ''' Randomizes the answer choices to simulate a completely random game. '''
        answer_choices_all = answer_choices.get(question_index)
        answer_choices_split = answer_choices_all.split('\n')
        answer_choices_randomized = '|'.join(
            [
                str(answer) for answer in random.sample(answer_choices_split,
                                                                            len(answer_choices_split))
            ])
        answer_choices_randomized_split = answer_choices_randomized.split('|')
        return answer_choices_randomized_split
        
    def verify_answer(self, abcd):
        ''' Verifies that the answer entered is possible. '''
        selected_answer = ''
        try:
            while selected_answer not in abcd:
                selected_answer = raw_input('Enter an answer choice: ')
        except KeyboardInterrupt:
                exit()
        return ord(selected_answer)
        
    def check_answer(self, question_index, selected_answer_text, answer_choices_dict, correct, total):
        ''' Checks the answer inputted from the player. '''
        if selected_answer_text == correct_answer[question_index]:
            print('{}'.format(random.choice(success_messages.values())))
            correct += 1
        else:
            for letter, text in answer_choices_dict.items():
                if text == correct_answer[question_index]:
                    print('{} The correct answer was: {} - {}.'.format(random.choice(failure_messages.values()),
                                                                                              letter,
                                                                                              text))
        total += 1
        print('Questions correct so far: {}/{}.\n'.format(correct,
                                                                               total))
        return correct, total
        
    def print_results(self, correct, total):
            ''' Prints the results of the Troovy game. '''
            if correct is 1:
                question_print_first = 'question'
            else:
                question_print_first = 'questions'
            if (total - correct) is 1:
                question_print_second = 'question'
            else:
                question_print_second = 'questions'
            print('You got {} {} correct and {} {} incorrect.'.format(correct,
                                                                                               question_print_first,
                                                                                               (total - correct),
                                                                                               question_print_second))
            print('Percentage correct: {}%. [{}/{}]'.format(self.calculate_percentage(correct,
                                                                                                            total),
                                                                                                            correct,
                                                                                                            total))
            print('Thanks for playing Troovy!')

    def calculate_percentage(self, correct, total):
        ''' Returns the percentage of correct answers of the Troovy game. '''
        try:
            return str(round(float(correct) / float(total) * 100, 2))
        except ZeroDivisionError:
            print('Woah! Division by zero! This should not happen!')
            return
            
    def check_choices(self):
        ''' Checks that correct_answer's values are in answer_choices's values since this is how Troovy checks the user's answer.
            This function runs before the game starts to make sure answers have not been tampered with. '''
        all_right = True
        for question in range(0, 99):
            if correct_answer[question] not in answer_choices[question]:
                print('{} is missing at index {}.'.format(correct_answer[question],
                                                              question))
                all_right = False
        if all_right:
            print('All answers found in answer choices! Starting Troovy Game!')
        else:
            print('Unable to start Troovy. Please fix the errors in the config file.')
            exit()

trv_game = troovyGame()
trv_game.troovy()