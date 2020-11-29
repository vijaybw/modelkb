# Foobar

Modelkb is a Python application which can be added to the project as library. It can automatically (1) extract and store the model's metadata-including its architecture, weights, and configuration; (2) visualize, query, and compare experiments; and (3) reproduce experiments.

## Installation

You can add the source-code to your project.


## Usage

```python
from modelkb import Experiment
exp = Experiment("PROJECTNAME", "YOUR NAME")
exp.track()
```
Please cite our Modelkb paper in your work if it helps you.

G. Gharibi, V. Walunj, S. Rella and Y. Lee, 
"ModelKB: Towards Automated Management of the Modeling Lifecycle in Deep Learning,"
 2019 IEEE/ACM 7th International Workshop on Realizing Artificial Intelligence Synergies in Software Engineering (RAISE),
 Montreal, QC, Canada, 2019, pp. 28-34, doi: 10.1109/RAISE.2019.00013.
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
