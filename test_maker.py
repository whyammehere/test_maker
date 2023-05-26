def test_maker(fileName):
    """Input the name of file containing correctly formatted questions"""

    from random import randint, uniform, seed, shuffle
    
    # seed the random numbers
    seed()

    # read text file and retrieve data
    with open(f"{fileName}", "r") as file:
        questions = file.read().split('\n\n')

    answer_key = []

    # create file to output test
    output_file = open('test_output.txt', 'w')

    # isolate each question in the file
    for question in questions:
        text = question.split('\n')
        
        prompt, FORMULA, input_vars = text[0], text[-1], text[1:-1]

        vars = {}

        for i in input_vars:
            x, min, max = i.split()

            if (float(min) % 1) == 0 and (float(max) % 1) == 0: 
                vars[x] = (int(min), int(max))
            else:
                vars[x] = (float(min), float(max))
        
        wrong_ans = []

        # generate answer choices within min and max
        i = 0
        while i < 4:
            temp_vars = {}

            decimal = False
            for j in vars:
                if type(vars[j][0]) == int:
                    temp_vars[j] = randint(vars[j][0],vars[j][1])
                else:
                    temp_vars[j] = format(uniform(vars[j][0],vars[j][1]),'.2g')
                    decimal = True

            temp_formula = FORMULA
            
            # isolate correct answer, format answers
            if i == 0:
                correct_vars = temp_vars

                for var in correct_vars.keys():
                    temp_formula = temp_formula.replace(var, str(correct_vars[var]))
            
                correct_ans = eval(temp_formula)
                
                if decimal:
                    if correct_ans < 0.1:
                        correct_ans = format(correct_ans,'.2e')
                    else:
                        correct_ans = format(correct_ans,'.2g')
                elif correct_ans >= 100000:
                    correct_ans = format(correct_ans,'.2e')
                i += 1
            else:
                for var in temp_vars.keys():
                    temp_formula = temp_formula.replace(var, str(temp_vars[var]))
                
                wrong_choice = eval(temp_formula)

                if decimal:
                    if wrong_choice < 0.1:
                        wrong_choice = format(wrong_choice,'.2e')
                    else:
                        wrong_choice = format(wrong_choice,'.2g')
                elif wrong_choice >= 100000:
                    wrong_choice = format(correct_ans,'.2e')
                
                if wrong_choice != correct_ans or round(float(wrong_choice), 2) == 0:
                    wrong_ans.append(wrong_choice)
                    i += 1
        
        # create list of all answers and shuffle
        temp_answers = [correct_ans] + wrong_ans
        shuffle(temp_answers)

        # create letter choices
        choices = 'abcd'
        answers = {}

        # assign anwers to letter choice
        for i in range(4):
            answers[choices[i]] = temp_answers[i]

            # append correct letter choice to answer key
            if temp_answers[i] == correct_ans:
                answer_key.append(choices[i])

        # create new prompt with variable values and write it to output file
        for var in correct_vars.keys():
            prompt = prompt.replace(f'`{var}`', str(correct_vars[var]))
        output_file.write(prompt + '\n')

        # write answer choices to output file
        for i in answers:
            output_file.write(f'{i}) {answers[i]}\n')
        output_file.write('\n')

    # line separation
    output_file.write('---------------------------------------\n\nAnswer Key:\n')

    # write answer key to output file
    for i, v in enumerate(answer_key):
        output_file.write(f'Q{str(i+1)}: {v}\n')

    # close file
    output_file.close()