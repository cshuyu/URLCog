import pymongo
import json, sys

class URLCogDBHandler():
    client = None #static variable for singleton pattern
    HOST_COLLECTION = "host-collection"
    DOMAIN_COLLECTION = "domain-collection"

    def __init__(self, config):
        if URLCogDBHandler.client == None:
            URLCogDBHandler.client = \
                pymongo.MongoClient(config['dbhost'], config['dbport'])
        self.db_name = config['dbname']
        self.db = URLCogDBHandler.client[self.db_name]
        dbs = set(self.db.collection_names())
        
        #create index
        #TODO: add statements if more collections are required.
        if not URLCogDBHandler.HOST_COLLECTION in dbs:
            self.__build_host_collection()
        if not URLCogDBHandler.DOMAIN_COLLECTION in dbs:
            self.__build_domain_collection()
        
        print "fetched db done.",str(self.db)
    
    def __clear(self, collection):
        self.db[collection].delete_many({})    

    def __build_domain_collection(self):
        ''' The domain collection records the information of
            all collected domains. Each domain corresponds to 
            one record.
            Index: domain (unique) 
        '''
        self.db[URLCogDBHandler.DOMAIN_COLLECTION].create_index([
            ('domain', pymongo.ASCENDING)], unique=True)

    def __build_host_collection(self):
        ''' The host collection records the information of
            all collected hosts. Each host corresponds to 
            one record.
            Index:  host (unique) 
                    domain
        '''
        self.db[URLCogDBHandler.HOST_COLLECTION].create_index([
            ('host', pymongo.ASCENDING)], unique=True)
        self.db[URLCogDBHandler.HOST_COLLECTION].create_index([
            ('domain', pymongo.ASCENDING)], unique=False)

    def __insert(self, collection, data):
        try:
            inserted_id = self.db[collection].insert_one(data)
        except Exception as e:
            print "error: insert failed: "+str(e)+" @"+str(data)
            return -1
        return inserted_id 

    def __query(self, collection, query):
        try:
            data = self.db[collection].find(query)
            rs = []
            for item in data:
                rs.append(item)
        except Exception as e:
            print "error: query failed: "+str(e)+" @"+str(query)
            return None
        return rs
    
    def __encode_data(self, data):
        failed = False
        try:
            new_data = {}
            for k in data: 
                v = data[k]
                if isinstance(k, str) or isinstance(k, unicode):
                    k = k.decode('utf-8')
                else:
                    k = str(k).decode('utf-8')
                if isinstance(v, str) or isinstance(v, unicode):
                    v = v.decode('utf-8')
                elif not (isinstance(v, int) or isinstance(v, float)):
                    v = str(v).decode('utf-8')
                new_data[k] = v
        except Exception as e:
            print "error: failed to encode data as UTF-8: "+str(e)
            failed = True
        if failed:
            try:
                print "     :"+str(data)
            except Exception as e:
                print "     : failed to display data: "+str(e)
            return None
        return new_data

    def insert_host_data(self, data):
        full_data = data
        if not isinstance(data, list):
            full_data = [data]
        count = 0
        #pre-processing
        for d in full_data:
            print str(d)
            if not 'host' in d:
                print "warning: failed inserting host data: host not exists."
                print "  ",str(d)
                continue
            if not "domain" in d:
                #TODO: extract domain from host and add it to d.
                pass 
            d = self.__encode_data(d)
            if d == None:
                continue
            inserted_id = self.__insert(URLCogDBHandler.HOST_COLLECTION, d)
            if inserted_id != -1:
                count += 1
        return count

    #TODO:
    def insert_domain_data(self, data):
        pass
    #TODO:
    def insert_XXX_data(self, data):
        pass

    #TODO:
    def find_host_data(self, data):
        pass
    #TODO:
    def find_domain_data(self, data):
        pass
    #TODO:
    def find_XXX_data(self, data):
        pass
                
        
    
def load_config(filename):
    ''' load the database configure file. '''
    with open(filename) as f:
        config = json.load(f)
    print "loaded settings: "+str(config)
    return config

def main():
    config = load_config(sys.argv[1])
    db_handler = URLCogDBHandler(config)
    
    #Debug
    v = db_handler.insert_host_data({'host':"www1.sina.com.cn", \
        "domain":"sina.com.cn", \
        "feature1":"somecontents", \
        "feature2":100})
    v += db_handler.insert_host_data({'host':"www2.sina.com.cn", \
        "domain":"sina.com.cn", \
        "feature1":"somecontents2", \
        "feature2":200})
    v += db_handler.insert_host_data({'host':"www1.sina.com.cn", \
        "feature1":"somecontents2", \
        "feature2":300})
    print str(v)

if __name__ == "__main__":
    main()