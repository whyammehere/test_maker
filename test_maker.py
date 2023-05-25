def test_maker(fileName, debug = False):  
    from random import randint, uniform, seed, shuffle
    
    seed()

    with open(f"{fileName}", "r") as file:
        questions = file.read().split('\n\n')

    answer_key = []
    for question in questions:
        text = question.split('\n')
        
        #print(text)
        prompt, FORMULA, input_vars = text[0], text[-1], text[1:-1]

        vars = {}
        #print(input_vars)
        for i in input_vars:
            x, min, max = i.split()
            if (float(min) % 1) == 0 and (float(max) % 1) == 0: 
                vars[x] = (int(min), int(max))
            else:
                vars[x] = (float(min), float(max))
        
        wrong_ans = []
        i = 0
        while i < 4:
            temp_vars = {}

            decimal = False
            for j in vars:
                if type(vars[j][0]) == int:
                    temp_vars[j] = randint(vars[j][0],vars[j][1])
                else:
                    #!ROUND
                    temp_vars[j] = format(uniform(vars[j][0],vars[j][1]),'.2g')
                    decimal = True

            temp_formula = FORMULA

            #print('temp:',temp_vars)
            
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
                i+=1
            else:
                
                for var in temp_vars.keys():
                    temp_formula = temp_formula.replace(var, str(temp_vars[var]))
                

                wrong_choice = eval(temp_formula)
                
                #print(temp_formula)
                #print(wrong_choice,wrong_choice<0.1)
                
                if decimal:
                    if wrong_choice < 0.1:
                        wrong_choice = format(wrong_choice,'.2e')
                    else:
                        wrong_choice = format(wrong_choice,'.2g')
                elif wrong_choice >= 100000:
                    wrong_choice = format(correct_ans,'.2e')
                
                if wrong_choice != correct_ans or round(float(wrong_choice),2) == 0:
                    wrong_ans.append(wrong_choice)
                    i += 1
            #print(i)
        
        temp_answers = [correct_ans] + wrong_ans
        answer_key.append(correct_ans)
        shuffle(temp_answers)
        choices = 'abcd'
        answers={}
        for i in range(4):
            answers[choices[i]] = temp_answers[i]

        for var in correct_vars.keys():
            prompt = prompt.replace(f'`{var}`', str(correct_vars[var]))

        if debug:
            print('debug:',FORMULA)
            print('debug:',temp_vars)


        print(prompt)
        print()
        for i in answers:
            print(f'{i}) {answers[i]}')
        print('\n')
        #print(f'\nanswer = {correct_ans}\n\n\n')

    print('Answer Key:')
    for i, v in enumerate(answer_key):
        print(f'{"Q"+str(i+1):{len(str(len(answer_key)))+1}}: {v}')


test_maker("test_maker.txt")
