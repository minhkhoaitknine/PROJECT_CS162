import json
import csv

class RouteVar:
    def __init__(self,data):
        self.RouteId=data['RouteId']
        self.RouteVarId=data['RouteVarId']
        self.RouteVarName=data['RouteVarName']
        self.RouteVarShortName=data['RouteVarShortName']
        self.RouteNo=data['RouteNo']
        self.StartStop=data['StartStop']
        self.EndStop=data['EndStop']
        self.Distance=data['Distance']
        self.Outbound=data['Outbound']
        self.RunningTime=data['RunningTime']
        
    def SetAttribute(self,attribute, value):
        setattr(self, attribute, value)
    
    def GetAttribute(self,attribute):
        return getattr(self, attribute)
        
class RouteVarQuery:
    def __init__(self, file_path):
        self.route_vars = []
        with open(file_path, 'r',encoding='utf-8') as file:
            for line in file:
                data = json.loads(line)
                for Coil in data:
                    RouteVar(Coil)
                    self.route_vars.append(RouteVar(Coil))
                
    def searchByAttributes(self, **kwargs):
        results = []
        for rv in self.route_vars:
            match = True
            for attribute, value in kwargs.items():
                if rv.GetAttribute(attribute) != value:
                    match = False
                    break
            if match==True:
                results.append(rv)
        return results

    def outputAsCSV(self, route_vars, filename):  # Modify method signature
        fieldnames = ['RouteId', 'RouteVarId', 'RouteVarName', 'RouteVarShortName',
                      'RouteNo', 'StartStop', 'EndStop', 'Distance', 'Outbound', 'RunningTime']

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:  # Specify UTF-8 encoding
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for route_var in route_vars:
                writer.writerow(route_var.__dict__)
                
    
    def outputAsJSON(self, route_vars, filename):
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            for route_var in route_vars:
                json.dump(route_var.__dict__, jsonfile, ensure_ascii=False)
                jsonfile.write('\n')


def main():     
    query=RouteVarQuery('D:/study/term_2/CS162/Lab/repository/PROJECT_CS162/source_code/vars.json')
    query.outputAsCSV(query.searchByAttributes(RouteId=3),'vars_CSV_file')
    query.outputAsJSON(query.searchByAttributes(RouteId=3),'vars_JSON_file')
if __name__=="__main__": 
    main() 