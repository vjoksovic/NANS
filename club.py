import data_functions

class Club():
  
  def __init__(self, name, passing, shooting, possession, predictions):
    self.name=name
    self.passing=passing
    self.shooting=shooting
    self.possession=possession
    self.predictions=predictions
    
  def passing_csv(self, folder):
    data_functions.dodavanje_to_csv(folder, self.name, self.passing)
    
  def shooting_csv(self, folder):
    data_functions.sutevi_to_csv(folder, self.name, self.shooting)
    
  def possession_csv(self, folder):
    data_functions.statistika_to_csv(folder, self.name, self.possession)
    
  def predictions_csv(self, folder):
    for prediciton in self.predictions:
      data_functions.predikcije_to_csv(folder, self.name, prediciton)
      
  def to_data(self):
    self.passing_csv("data")
    self.shooting_csv("data")
    self.possession_csv("data")
    self.predictions_csv("data")
    
  def to_test(self):
    self.passing_csv("test")
    self.shooting_csv("test")
    self.possession_csv("test")
    #self.predictions_csv("test")