import json
import re
import random
import string

class PasswordGenerator:

    def __init__(self, config: str):
        self.rules = config
        self.length = self.rules['length']
        self.allowed_characters_dict = self.rules['allowed_characters']
        self.required_characters = self.rules['required_characters']
    #  begin internal methods used to generate new password
    def _generate_random_index(self, max_length):
        return random.randint(0, max_length - 1)

    def _group_generator(self, max_length, chars):
        return ''.join(random.choice(chars) for _ in range(max_length))

    def _handle_rule(self, required_rule, characters_dict):
        count = required_rule[0]
        section_type = f"{required_rule[1]}s"
        section = required_rule[-1]
        sub_section = characters_dict[section_type][section]
        section_length = len(sub_section)

        if section_type == 'groups':
            result = ''
            for i in range(count):
                random_index = self._generate_random_index(section_length)
                result += sub_section[random_index]
            return result

        if section_type == 'constants':
            match sub_section:
                case 'ascii_lowercase':
                    return self._group_generator(count, string.ascii_lowercase)
                case 'ascii_uppercase':
                    return self._group_generator(count, string.ascii_uppercase)
                case 'digits':
                    return self._group_generator(count, string.digits)

    #   end: internal methods for generating password

    #   begin: internal methods for validating passwords
    def _validate_consecutive(self, password, max_allowed):
        consecutive_occurrences = {}
        for char in password:
            count = 1
            if char in consecutive_occurrences.keys():
                count += consecutive_occurrences[char]
                if count > max_allowed:
                    print(f"{char} occured more than {max_allowed} times")
                    return False
            consecutive_occurrences[char] = count
        return True

    def _validate_occurrence(self, password, max_allowed):
        occurrences = [password.count(char) for char in password]
        if max(occurrences) > max_allowed:
            print(
                f"cannot have more than {max_allowed} of any character")
            return False
        return True
    def _handle_rule_for_validation(self, allowed_characters_type, allowed_characters_subtype, allowed_characters_dict):
        if allowed_characters_type == 'groups':
            return allowed_characters_dict[allowed_characters_type][allowed_characters_subtype]
            
        if allowed_characters_type == 'constants':
            string_type = allowed_characters_dict[allowed_characters_type][allowed_characters_subtype]
            
            match string_type:
                case 'ascii_lowercase':
                    return string.ascii_lowercase
            match string_type:
                case 'ascii_uppercase':
                    return string.ascii_uppercase
            match string_type:
                case 'digits':
                    return string.digits

    def _get_all_allowed_chars(self):
        allowed_characters_dict = rules['allowed_characters']
        allowed_characters_string = ''
        for allowed_characters_type in allowed_characters_dict:
            for allowed_characters_subtype in allowed_characters_dict[allowed_characters_type]:
                allowed_characters_string += self._handle_rule_for_validation(allowed_characters_type, allowed_characters_subtype, allowed_characters_dict)
        return allowed_characters_string

    def _check_required_characters(self, required_rule, password, allowed_characters_dict):
        allowed_characters_type = f"{required_rule[1]}s"
        allowed_characters_subtype = required_rule[-1]
        # using handler functions to extract the string with which to compare password with
        group = self._handle_rule_for_validation(allowed_characters_type, allowed_characters_subtype, allowed_characters_dict)
        print(group)

        # validate that the password contains at least the number of instances of the specified characters in given rule 
        required_count = required_rule[0]
        count = 0
        for char in password:
            count += group.count(char)
            
        if count < required_count:
            print(
                f'Password violation:\nyou need at least {required_count} {allowed_characters_subtype}')
            return False

        return True
    # create the base of the password based on required characters
    def _generate_base(self):

        return

    #   end: internal methods for validating passwords

    #   Begin: public methods

    def new(self) -> str:

        print(self.required_characters)
        length = self.rules['length']
        allowed_characters_dict = self.rules['allowed_characters']
        required_characters = self.rules['required_characters']
        print(self.required_characters)
        # creates base password from required and allowed characters
        password = ''
        for required_rule in self.required_characters:
            password += self._handle_rule(required_rule, self.allowed_characters_dict)

        # if password lenght is equal to required length, return password
        if len(password) == length:
            return password

        # All other rules have been satisfied apart from length.
        # Adds random ascii letters to the end of the password,
        # only if they aren't present in the password already. This,
        # ensures that there won't be any violations (consecutive & occurence).
        ascii_letters = string.ascii_letters 
        for _ in ascii_letters:
            random_index = self._generate_random_index(len(ascii_letters))
            char = ascii_letters[random_index]
            if char not in password:
                password += char
            if len(password) == length:
                return password

        return password

    

    def allowed(self, password: str) -> bool:
        # Check Length
        length_requirement = self.rules['length']
        if len(password) < length_requirement:
            print(f'{password} length is < {length_requirement}')
            return False

        # Deal with violations
        #
        violations = self.rules['violations']
        banned_words = violations['verboten']
            # I'm assuming the word is banned regardless of casing
        if password.lower() in banned_words: # Check verboten
            print(f"'{password}' is not allowed as a password")
            return False

        
        max_allowed_consecutive = violations['consecutive']
        if not self._validate_consecutive(password, max_allowed_consecutive): # check violations > consecutive
            return False

        
        max_allowed_occurrence = violations['occurrence'] 
        if not self._validate_occurrence(password, max_allowed_occurrence): # check violations > occurances
            return False

        # check allowed characters
        #
        allowed_characters_dict = rules['allowed_characters']
        required_characters = rules['required_characters']
        allowed_characters = self._get_all_allowed_chars() #gets merged string of all allowed characters
        for char in password:
            if char not in allowed_characters:
                print(f'{char} is not allowed')
                return False

        # check required_characters
        #
        for required_rule in required_characters:
            validated = self._check_required_characters(required_rule, password, allowed_characters_dict)
        return validated




FILENAME = './././config_strong.json'
def getRules(filename):
    rules = {}
    with open(filename, 'rt') as json_string:
        rules = json.load(json_string)
    return rules


rules = getRules(FILENAME)

newPassword = PasswordGenerator(rules)
new_password = newPassword.new()

print(new_password)
print(newPassword.allowed('#JOao26XbtEj'))