import unittest
from team_Artiom_Bikalpa_Seifalislam_model import library

class libraryTest(unittest.TestCase):
    def setUp(self):
        self.testLib = library()
        self.name = "team_Artiom_Bikalpa_Seifalislam_lib_default.json"
        self.name1 = "empty.json"
        self.name2 = "asdf.json"
    
    def test_open(self):
        self.assertIsNone(self.testLib.init(self.name)) #Checks if the file can be opened and parsed
        self.assertIsNone(self.testLib.init(self.name2)) #Test to read a file without read permission
    
    def test_save(self):
        self.testLib.init(self.name)
        self.assertTrue(self.testLib.save()) #tests for saving the json
    
    def test_empty_save(self):
        self.testLib.init(self.name1)
        self.assertTrue(self.testLib.save()) #tests for saving an empty json
    
    def test_addBook(self):
        self.testLib.init(self.name1)
        self.assertIsNone(self.testLib.addBook("name", "author", "123", "status"))

if __name__ == "__main__":
    unittest.main()
