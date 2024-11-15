def format_output():
    file_path = 'output.txt'

    with open(file_path, 'r', encoding='utf-8') as infile:
        
        lines = infile.readlines()

        subject = f'Предмет: {lines[0].strip()}'
        teacher = f'Преподаватель: {lines[1].strip()}'
        room = f'Аудитория: {lines[2].strip()}'

        result = f'echo "{subject}\n{teacher}\n{room}"'

        with open(file_path, 'w', encoding='utf-8') as outfile:
            outfile.write(result + '\n')
