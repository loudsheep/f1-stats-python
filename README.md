# F1 Stats Backend API - Formula 1 Statistics API

![F1 Stats Backend API](https://github.com/loudsheep/f1-stats-react/blob/master/src/assets/f1_stats.jpg)

F1 Stats Backend API is a Python (Flask) application that serves as the backend for the F1 Stats website. This API provides essential data and functionalities to the frontend, allowing users to access and interact with Formula 1 race results, driver standings, points, and telemetry data. With F1 Stats Backend API, you can effortlessly power your F1 Stats frontend and deliver real-time Formula 1 information to your users.

## Introduction

F1 Stats Backend API is designed to work in conjunction with the F1 Stats frontend, providing a seamless experience for users interested in exploring Formula 1 statistics and telemetry data. By leveraging Python and Flask, the API delivers efficient and reliable data to the frontend, ensuring a smooth user experience.

## Features

- Exposes endpoints to retrieve race results, driver standings, points, and telemetry data.
- Implements secure authentication mechanisms to protect sensitive data and endpoints.
- Efficiently interacts with a database to store and retrieve Formula 1 data for optimal performance.
- Handles API requests from the frontend and provides timely responses for a seamless user experience.

## Installation

To set up and run F1 Stats Backend API on your local machine, follow these steps:

1. Clone the repository to your local machine using the following command:

```
git clone https://github.com/loudsheep/f1-stats-python.git
```

2. Navigate to the project directory:

```
cd f1-stats-python
```

3. Install the required dependencies:

```
pip install -r requirements.txt
```

## Usage

To run F1 Stats Backend API, execute the following command:

```
python app.py
```

The API will be accessible at `http://localhost:5000/`. It is designed to handle API requests from the F1 Stats frontend and deliver relevant data in response.

## Endpoints

F1 Stats Backend API exposes the following endpoints:

- `/schedule`: Retrieve current Formula 1 season race schedule
- `/winners`: Driver current points and max possible points to gain this season
- `/sessions/<int:year>`: Get session names of every race in the season(year).
- `/results/<int:year>/<int:event>/<string:session>`: Results of the specified session. Points, positions, finishing status.
- `/tires/<int:year>/<int:event>/<string:session>`: Tire data for session.
- `/laps/<int:year>/<int:event>/<string:session>/<string:driver>`: Lap times for every driver in a session.
- `/lap-leaders`: Number of laps led in a race for every driver in current season.
- `/heatmap/<int:year>/<string:category>`: Data for heatmap of points.
- `/telemetry/<int:year>/<int:event>/<string:session>/<string:driver>/<int:lap>`: Obtain telemetry data from races, including lap times, speeds, and more.

## Contributing

We welcome contributions to enhance the functionality and performance of F1 Stats Backend API. To contribute, please follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch with a descriptive name for your feature/bugfix.
3. Make your changes and commit them with a clear message.
4. Push your changes to your fork.
5. Submit a pull request to the original repository.

We will review your pull request and merge it if everything looks good.

## License

This project is licensed under the [GPL-3.0 License](LICENSE), which means you are free to use, modify, and distribute the code. Attribution is not required, but it's appreciated.

---

Thank you for using F1 Stats Backend API to power your F1 Stats frontend. We hope this API facilitates a seamless experience for your users and provides them with valuable Formula 1 insights. If you have any questions or encounter issues, please don't hesitate to open an issue on the repository. Happy coding!