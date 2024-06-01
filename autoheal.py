from selenium import webdriver
import requests
import difflib
import linecache
import gensim
import gensim.downloader as api
from nltk.tokenize import word_tokenize
import pandas as pd


class AutoHealTest:

    def __init__(self,subject_name, attendance):
        linecache.clearcache()
        self.a = attendance
        self.s = subject_name
        try:
            self.test_without_heal(self.a, self.s)
            print('Everything works with no change in locator elements')
        except Exception as e:
            self.after_locator_change()
            print("something was changed")
            self.prior_to_locator_change()



    def test_without_heal(self,subject_name, attendance):
        driver = webdriver.Chrome()

        #navigate to the webpage
        driver.get("https://balgiproject.herokuapp.com/")

        #launch app and fill form and submit
        driver.find_element("id", "subject").send_keys(subject_name)
        driver.find_element("id", "attendance").send_keys(attendance)
        driver.find_element("xpath", "//button[@class='btn btn-primary']").send_keys(subject_name).click()

    
    
    def after_locator_change(self):
        url = "https://balgiproject.herokuapp.com/"

        page = requests.get(url)
        with open('changed_new.html', 'wb+') as f:
            f.write(page.content)
        file1="initial.html"
        file2="changed_new.html"

        diff = difflib.ndiff(open(file1).readlines(), open(file2).readlines())
        a = ''.join(diff)
        prior_to_locator_change = []
        self.line_no_changed = []
        after_locator_change = []

        for val,i in enumerate(a.split('\n')):
            if i[0]=='-':
                prior_to_locator_change.append(i)
                self.line_no_changed.append(val)
            else:
                after_locator_change.append(i)
        
        lineval = []
        with open('changed_new.html') as f:
            for val, i in enumerate(self.line_no_changed):
                if val==0:
                    lineval.append(linecache.getline('changed_new.html',i+1)[14:])
                else:
                    lineval.append(linecache.getline('changed_new.html',i-(val))[14:])

            
        self.linevalnew = list(filter(('   \n').__ne__, lineval))
        return self.linevalnew


    
    def prior_to_locator_change(self):

        url = "https://balgiproject.herokuapp.com/"

        page = requests.get(url)
        with open('initial.html', 'wb+') as f:
            f.write(page.content)

        linevalwas=[]
        with open('initial.html') as f:
            for val,i in enumerate(self.line_no_changed):
                if val==0:
                    linevalwas.append(linecache.getline('initial.html', i+1))
                else:
                    linevalwas.append(linecache.getline('initial.html', i-(val)))
        self.linevalnewwas = list(filter(('        \n').__ne__, linevalwas))
        return self.linevalnewwas
    
    def doc2vecnew(self):
        docvec=[]
        datimp = pd.read_excel('titles1.xlsx')
        dataset = datimp.Titles
        data = [d for d in dataset]
        def tagged_document(list_list_of_words):
            for i, list_of_words in enumerate(list_list_of_words):
                yield gensim.models.doc2vec.TaggedDocument(list_of_words, [i])
        data_for_training = list(tagged_document(data))
        model = gensim.models.doc2vec.Doc2Vec(vector_size=40, min_count=2, epochs=30)
        model.build_vocab(data_for_training)
        model.train(data_for_training, total_examples=model.corpus_count, epochs=model.epochs)

        for i in self.linevalnew:
            tokens = word_tokenize(str(i))
            docvec.append(model.infer_vector(tokens))
        print("Doc2Vec vec for updated build")
        print(docvec)


    def doc2vecold(self):
        docvec=[]
        datimp = pd.read_excel('titles1.xlsx')
        dataset = datimp.Titles
        data = [d for d in dataset]
        def tagged_document(list_list_of_words):
            for i, list_of_words in enumerate(list_list_of_words):
                yield gensim.models.doc2vec.TaggedDocument(list_of_words, [i])
        data_for_training = list(tagged_document(data))
        model = gensim.models.doc2vec.Doc2Vec(vector_size=40, min_count=2, epochs=30)
        model.build_vocab(data_for_training)
        model.train(data_for_training, total_examples=model.corpus_count, epochs=model.epochs)

        for i in self.linevalnewwas:
            tokens = word_tokenize(str(i))
            docvec.append(model.infer_vector(tokens))
        print("Doc2Vec vec for previous build")
        print(docvec)


    def autoheal(self,subject_name, attendance):
        vals=[]
        got = a.after_locator_change()
        for i in got:
            vals.append(i.split()[4][4:-1])
            driver = webdriver.Chrome()

            #navigate to the webpage
            driver.get("https://balgiproject.herokuapp.com/")

            #launch app and fill form and submit
            driver.find_element("id", vals[0]).send_keys(subject_name)
            driver.find_element("id", vals[1]).send_keys(attendance)
            driver.find_element("xpath", "//button[@class='btn btn-primary']").send_keys(subject_name).click()

        return a.after_locator_change()


a = AutoHealTest("GH", 97)
a.doc2vecnew()
