import os


def load_questions_answers(folder_path):
    folder_path = os.path.join(os.path.dirname(__file__), folder_path)
    all_questions_answers = {}
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'rt', encoding='KOI8-R') as file:
            file_content = file.read().split('\n\n')
        questions = []
        answers = []
        for block in file_content:
            if block.startswith('Вопрос'):
                question_lines = block.split('\n')[1:]
                question_text = ' '.join(question_lines)
                questions.append(question_text)
            if block.startswith('Ответ'):
                answer_lines = block.split('\n')[1:]
                answer_text = ' '.join(answer_lines)
                answers.append(answer_text)
        questions_answers = dict(zip(questions, answers))
        all_questions_answers.update(questions_answers)
    return all_questions_answers
