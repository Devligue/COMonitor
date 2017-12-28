# COMonitor

COMonitor is a multiplatform tray application to monitor connections and disconnections of serial ports (COM ports), written in PyQt.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to run COMonitor and how to install them.

#### Python 3

If you are sporting one of the newer Linux distributions chances are you already have it. For everyone else: go to [python.org/downloads](https://www.python.org/downloads/), choose latest Python 3 version and install it.

If you are not sure what version you have, type the following command into terminal:

    $ python

#### Packages

Once you are sure your Python 3 is up and good, its time to install some requirements. In the root directory of this application you will find `requirements.txt` file. It contains all Python packages names that need to be installed. To do it simply and fast go to the **COMonitor** root directory and use:

    $ sudo pip install -r requirements.txt

### Using COMonitor

COMonitor does not require any installation. Once your prerequisites are in place you are ready to go. To start the application open its root directory and use:

    $ ./comonitor.py

or

    $ python ./comonitor.py

## Running the tests

Glad you ask. Tests are located in `test` directory. You can invoke them with:

    $ pytest

## Deployment

To make best use of COMonitor, add it to startup applications. You will never have to worry about what is the name of port you are plugging in to your machine.

## Contributing

TODO

## Versioning

We use [SemVer](http://semver.org/) for versioning.

## Authors

-   **Krzysztof Dziadowiec**

## License

This project is licensed under the GNU General Public License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

-   This project was developed during the Scripting Languages course on AGH University of Science and Technology (Winter 2017/2018).
