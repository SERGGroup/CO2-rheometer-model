# sCO<sub>2</sub> Rheometer Model
_(developed by the [SERG group](https://www.dief.unifi.it/vp-177-serg-group-english-version.html) of the [University of Florence](https://www.unifi.it/changelang-eng.html) in the scope of the [HOCLOOP project](https://www.hocloop.eu/))_

### Model Description 👩‍💻
The model was intended to evaluate if a particular rheometer can reach a __specific supercritical state__ (in terms of _pressure and temperature_) __starting from the CO<sub>2</sub> extracted from a 60bar cylinder__. 

The superctitical state is expected to be reached trough a __insochoric transformation__ (in wich the CO<sub>2</sub> inside the rheomether is heated up and consequently pressurized).

The model can provide the researcher with the information regarding:

- Whether a specific state __can be reached__
- __The filling temperature to be set__ in order to reach that state
- The __uncertanties__ associated with the specific procedure


### Folder Organizarion 📂

- the _main_code_ folder contains the classes developed to model the reometer, in particular:
  -  the file _rheometer.py_ contains the _Rheometer_ class that performs all the calculation required for the model to work
  -  the _support_ folder contains support classes of functions

- the _calculation_ folder contains the code that can be used to get the results from the model

