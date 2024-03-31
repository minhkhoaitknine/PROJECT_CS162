import json
import csv

class Stop:
    def __init__(self, data):
        self.StopId = data['StopId']
        self.Code = data['Code']
        self.Name = data['Name']
        self.StopType = data['StopType']
        self.Zone = data['Zone']
        self.Ward = data['Ward']
        self.AddressNo = data['AddressNo']
        self.Street = data['Street']
        self.SupportDisability = data['SupportDisability']
        self.Status = data['Status']
        self.Lng = data['Lng']
        self.Lat = data['Lat']
        self.Search = data['Search']
        self.Routes = data['Routes']
        
    def SetAttribute(self,attribute, value):
        setattr(self, attribute, value)
        
    def GetAttribute(self,attribute):
        return getattr(self, attribute)
   
class StopQuery:
    def __init__(self, file_path):
        self.stops = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                data = json.loads(line)
                stops_data = data.get('Stops', [])
                for stop_data in stops_data:
                    stop = Stop(stop_data)
                    self.stops.append(stop)
            
                
    def searchByAttributes(self, **kwargs):
        results = []
        for stop in self.stops:
            match = True
            for attribute, value in kwargs.items():
                if stop.GetAttribute(attribute) != value:
                    match = False
                    break
            if match==True:
                results.append(stop)
        return results

    def outputAsCSV(self, stops, filename):  # Modify method signature
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:  # Specify UTF-8 encoding
            fieldnames = ['StopId', 'Code', 'Name', 'StopType', 'Zone', 'Ward', 'AddressNo', 'Street', 
                          'SupportDisability', 'Status', 'Lng', 'Lat', 'Search', 'Routes']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for stop in stops:
                writer.writerow(stop.__dict__)
                
    
    def outputAsJSON(self, stops, filename):
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            for stop in stops:
                json.dump(stop.__dict__, jsonfile, ensure_ascii=False)
                jsonfile.write('\n')

def main():  
    query=StopQuery('D:/study/term_2/CS162/Lab/repository/PROJECT_CS162/source_code/stops.json')
    query.outputAsCSV(query.searchByAttributes(StopId=3),'stop_CSV_file')
    query.outputAsJSON(query.searchByAttributes(StopId=3),'stop_JSON_file')
if __name__=="__main__": 
    main() 