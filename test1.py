import us

if __name__ == "__main__":
    vowels = set(list('aeiouAEIOU'))
    state_names = [x.name for x in us.states.STATES]
    longest_state_len = len(sorted(state_names, key=lambda word: len(word), reverse=True)[0])    

    word = ''
    for state_name in state_names:
        word_order = 'AFTER'

        if state_name[0] in vowels and state_name[-1] in vowels:
            word_order = 'BEFORE'
            word = 'VooDoo'
        else:
            if state_name[0] in vowels:
                word = 'Voo'
            else:
                if state_name[-1] in vowels:
                    word = 'Doo'

        print_str_format = '%' + str(longest_state_len) + 's '
        print_str_format += print_str_format
        if word_order == 'AFTER':
            print print_str_format % (state_name, word)
        elif word_order == 'BEFORE':
            print print_str_format % (word, state_name)
        else:
            raise Exception("Unknown word order: %s" % word_order)
