import us

if __name__ == "__main__":
    vowels = set(list('aeiouAEIOU'))
    state_names = [x.name for x in us.states.STATES]
    longest_state_len = len(sorted(state_names, key=lambda word: len(word), reverse=True)[0])

    word = ''
    for state_name in state_names:
        num_vowels = len([c for c in state_name if c in vowels])
        num_consonants = len([c for c in state_name if c not in vowels])

        word_order = 'AFTER'

        if num_vowels > num_consonants:
            word = "Apple"
        else:
            if num_vowels < num_consonants:
                word = "Pie"
            else:
                if num_vowels == num_consonants:
                    word = "Apple Pie"
                    word_order = 'BEFORE'

        if ' ' in state_name:
            state_name = state_name.upper()
            word = word.upper()

        print_str_format = '%' + str(longest_state_len) + 's '
        print_str_format += print_str_format
        if word_order == 'AFTER':
            print print_str_format % (state_name, word)
        elif word_order == 'BEFORE':
            print print_str_format % (word, state_name)
        else:
            raise Exception("Unknown word order: %s" % word_order)
