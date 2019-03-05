class Node():

    def __init__(self):
        self.children_node = {}
        self.total_word_so_far = ''
        self.current_letter = ''
        self.word = ''
        self.current_index = 0
        self.id = 0


    def add_word_to_trie(self, word, id, word_so_far='', curr_index=-1):
        self.word = word
        self.current_index = curr_index
        self.id = id
        if self.current_index >= 0:
            self.current_letter = self.word[self.current_index]
            self.total_word_so_far = word_so_far + self.word[self.current_index]
        
        if self.current_index + 1 < len(self.word):
            if self.word[self.current_index + 1] not in self.children_node:
                self.children_node[self.word[self.current_index+1]] = Node()
                self.children_node[self.word[self.current_index+1]].add_word_to_trie(\
                    self.word, self.id, self.total_word_so_far, self.current_index+1)

            else:
                self.children_node[self.word[self.current_index+1]].add_word_to_trie(\
                    self.word, self.id, self.total_word_so_far, self.current_index+1)


    def auto_complete_word(self, new_word):
        response = None
        if len(new_word) > 0 and new_word[0] in self.children_node:
            response = self.children_node[new_word[0]].auto_complete_word(new_word[1:])   
        if len(new_word) == 0:
           response = self.find_word([])
        return response 
            

    def find_word(self, auto_completed_word_list=[]):
        if self:
            if len(self.children_node) == 0:
                auto_completed_word_list.append({'name':self.total_word_so_far, 'id':self.id})
            else:
                for child_node in self.children_node:
                    auto_completed_word_list = self.children_node[child_node].find_word(auto_completed_word_list)

        return auto_completed_word_list


def autocomplete_main(search_key, data):
    root = Node()
    response = None
    if len(root.children_node) == 0:
        for i in data:
            root.add_word_to_trie(i.get("name").lower(), i.get("id"))
        response = root.auto_complete_word(search_key.lower())       
    else:
        response =  root.auto_complete_word(search_key.lower())
    return response
    