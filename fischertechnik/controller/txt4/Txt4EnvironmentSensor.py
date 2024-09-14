import sys
import threading
import time

from bme680 import BME680
from smbus import SMBus

from ..EnvironmentSensor import EnvironmentSensor


class Txt4EnvironmentSensor(EnvironmentSensor):
    """
    A facade for easy access to Bosch's BME680 environment sensor.

    Underlying class is the BME680 class from pimoroni.
    """

    __TIME_TO_WAIT_FOR_SENSOR_DATA_TO_STABILIZE = 300
    __HUMIDITY_BASE_VALUE = 40
    __HUMIDITY_WEIGHT = 25
    __GAS_WEIGHT = 75
    __heatup_temperature = 320
    __heatup_time = 150

    def __init__(self, controller, identifier):
        """
        Initializes the Txt2EnvironmentSensor.

        Parameters taken from superclass.

        @param controller the TXT controller. Needs to be supplied in order to be compatible with the superclass __init__ method, but will be discarded
        @param identifier The number of the input. Necessary to be compatible with the superclass. Must be supplied but is not used.
        """
        EnvironmentSensor.__init__(self, controller, identifier)
        self.__bme680 = BME680(i2c_device=SMBus(3))
        self.__gas_base_value = None
        self._calibrated = False
        self.__accuracy = 0
        self.__calibration_thread = None

    @property
    def heatup_temperature(self) -> int:
        """
        The target temperature of the sensor while measuring gas resistance.

        @returns {int} the last set heatup temperature (default: 320 °C)
        """
        return Txt4EnvironmentSensor.__heatup_temperature

    @heatup_temperature.setter
    def set_heatup_temperature(self, value):
        """
        Sets the target temperature of the sensor when measuring gas resistance.
        @param {int} the heatup temperature. Must be in range [200, 400].
        """
        if value < 200 or value > 400:
            raise ValueError('The heater temperature is supposed to be in range(200, 400)')

        Txt4EnvironmentSensor.__heatup_temperature = value

    @property
    def heatup_time(self) -> int:
        """
        The time  in milliseconds for which the heater runs to heat up the sensor during
        gas resistance measurement.

        If this time is too short, the heater might not heat up the sensor fully to the
        target temperature.

        @returns {int} heatup time in milliseconds (default: 150ms)
        """
        return Txt4EnvironmentSensor.__heatup_time

    @heatup_time.setter
    def set_heatup_time(self, value):
        """
        Set the heatup time.

        @param {int} value: the heatup time in milliseconds, cannot be negative
        """
        if value < 0:
            raise ValueError('Time cannot be negative')

        Txt4EnvironmentSensor.__heatup_time = value

    @property
    def calibrated(self) -> bool:
        """
        Returns whether sensor is calibrated or not.

        @returns {bool}
        """
        return self._calibrated

    def _iaq_setup(self):
        """
        Calibrates the sensor by heating up the sensor to measure gas values while heating up.
        The average of the last 50 gas values will be taken as gas baseline value.
        The difference of the current gas resistance and the gas baseline value will be used
        to determine the air quality.

        WARNING: This method takes five minutes to complete. Progress will be shown on the
        console/terminal if the program is run in a console/terminal. If you want to do something
        else while the sensor calibrates, you should call this method in a thread.
        """

        self.__accuracy = 0

        # heat up gas sensor
        self.__bme680.set_gas_heater_temperature(self.heatup_temperature)
        self.__bme680.set_gas_heater_duration(self.heatup_time)
        self.__bme680.select_gas_heater_profile(0)

        start_time = time.time()
        curr_time = time.time()

        last_gas_values = []

        # collect gas sample values for __TIME_TO_WAIT_FOR_SENSOR_DATA_TO_STABILIZE / 60 minutes
        print('Calibrating your sensor. This will take {:.0f} minutes. Please wait.'.format(Txt4EnvironmentSensor.__TIME_TO_WAIT_FOR_SENSOR_DATA_TO_STABILIZE // 60))
        self.__accuracy = 2
        while (curr_time - start_time) < Txt4EnvironmentSensor.__TIME_TO_WAIT_FOR_SENSOR_DATA_TO_STABILIZE:
            curr_time = time.time()
            if self.__bme680.get_sensor_data() and self.__bme680.data.heat_stable:
                if int(curr_time - start_time) % int(Txt4EnvironmentSensor.__TIME_TO_WAIT_FOR_SENSOR_DATA_TO_STABILIZE * 0.05) == 0:
                    # show progress on terminal every 5%
                    print('{0:3.0f} seconds remaining ({1:03.0f}% done)'.format(Txt4EnvironmentSensor.__TIME_TO_WAIT_FOR_SENSOR_DATA_TO_STABILIZE - (curr_time - start_time), (curr_time - start_time) * 100 / Txt4EnvironmentSensor.__TIME_TO_WAIT_FOR_SENSOR_DATA_TO_STABILIZE))
                gas = self.__bme680.data.gas_resistance
                last_gas_values.append(gas)
                time.sleep(1)

        # calculate gas base value as average of the last 50 gas values
        self.__gas_base_value = sum(last_gas_values[-50:]) / 50.0
        self.__accuracy = 3
        print('Done!')
        self._calibrated = True

    def _calc_iaq(self) -> float:
        """
        Determines the air quality using the current relative humidity and
        current gas resistance.

        It is not supposed to be used by users using the public interface.

        @deprecated Do not use directly. Call get_indoor_air_quality_as_text(self) or
        get_indoor_air_quality_as_number(self) instead.

        @returns {float} a number representing air quality
        """

        if not self.calibrated:
            self.calibrate()
            return -1

        gas = self.__bme680.data.gas_resistance
        gas_offset = self.__gas_base_value - gas

        hum = self.__bme680.data.humidity
        hum_offset = hum - Txt4EnvironmentSensor.__HUMIDITY_BASE_VALUE

        self.__bme680.get_sensor_data()
        if self.__bme680.data.heat_stable:
            if hum_offset > 0:
                hum_score = (100 - Txt4EnvironmentSensor.__HUMIDITY_BASE_VALUE - hum_offset)
                hum_score /= (100 - Txt4EnvironmentSensor.__HUMIDITY_BASE_VALUE)
                hum_score *= Txt4EnvironmentSensor.__HUMIDITY_WEIGHT

            else:
                hum_score = (Txt4EnvironmentSensor.__HUMIDITY_BASE_VALUE + hum_offset)
                hum_score *= Txt4EnvironmentSensor.__HUMIDITY_WEIGHT / Txt4EnvironmentSensor.__HUMIDITY_BASE_VALUE

                # Calculate gas_score as the distance from the gas_baseline.
            if gas_offset > 0:
                gas_score = (gas / self.__gas_base_value)
                gas_score *= Txt4EnvironmentSensor.__GAS_WEIGHT
            else:
                gas_score = Txt4EnvironmentSensor.__GAS_WEIGHT

            return hum_score + gas_score
        return -1

    def needs_calibration(self) -> bool:
        """
        Returns whether the sensor needs calibration.

        @returns {bool}
        <ul>
            <li>True if the sensor is NOT calibrated</li>
            <li>False if the sensor is calibrated</li>
        </ul>
        """
        return not self.calibrated

    def get_accuracy(self) -> int:
        """
        Returns the current accuracy value, defined by BOSCH Sensortec API.

        Legacy method which simulates the return of an accuracy value, as defined by the BOSCH
        Sensortec API.

        Instead the accuracy is set to 0 at the initialization,
                                    to 2 before the calibration has finished and
                                    to 3 after the calibration has finished

        Meaning, according to BOSCH Sensortec library:
        0: Sensor is not calibrated
        1: Data has been stable, calibration of sensor is uncertain
        2: Sensor calibrates
        3: Sensor is calibrated

        @returns {int}
        <ul>
            <li>0 before _iaq_setup is called</li>
            <li>2 before _iaq_setup performs the calibration</li>
            <li>3 when _iaq_setup has finished the calibration</li>
        </ul>
        """
        return self.__accuracy

    def get_temperature(self) -> float:
        """
        Returns the current temperature in °C.

        @returns {float}
        """
        self.__bme680.get_sensor_data()
        return self.__bme680.data.temperature

    def get_humidity(self) -> float:
        """
        Performs a measurement and returns the relative humidity in %.

        @returns {float}
        """
        self.__bme680.get_sensor_data()
        return self.__bme680.data.humidity

    def get_pressure(self) -> float:
        """
        Returns the air pressure in hectopascal (hPa).

        @returns {float}
        """
        self.__bme680.get_sensor_data()
        return self.__bme680.data.pressure

    def calibrate(self):
        """
        Starts a thread to calibrate the sensor.

        This method is not necessary, as the calibration is automatically called by the
        get_indoor_air_quality_as_text(self) and get_indoor_air_quality(self) methods
        if the sensor was not calibrated prior to calling these methods, but they call
        the calibration method in the calling/main thread, not in a seperate thread, which will
        render your calling thread/main thread unable to do anything else in the next five
        minutes.

        It is usually wise to call this method if you want to do anything else while the sensor
        calibrates.

        You can use the is_ready(self) or needs_calibration(self) methods if you want to know
        if the calibration thread has finished.
        """
        if self.__calibration_thread and self.__calibration_thread.is_alive():
            return
        self.__calibration_thread = threading.Thread(target=self._iaq_setup)
        self.__calibration_thread.start()

    def is_ready(self) -> bool:
        """
        Returns whether the calibration thread has finished.

        To be called after calibrate.

        @return {bool} whether the calibration thread is finished.
        Returns False if the calibration thread has never started.
        """
        if not self.__calibration_thread is None:
            return not self.__calibration_thread.is_alive()
        return False

    def get_indoor_air_quality_as_text(self) -> str:
        """
        Returns an assessment of the current air quality, such as "Good" or
        "Very bad".

        @returns {str} the indoor air quality as text

        @throws MissingValueException if the sensor was not calibrated before this method
        was called
        @throws MeasurementException if measuring failed
        @throws ValueError if an internal error happened which caused the indoor air quality
        values to be out of range
        """
        return _get_iaq_as_text(self._calc_iaq())

    def get_indoor_air_quality_as_number(self) -> float:
        """
        Returns an indoor air quality index, ranging from 0 to 500, where
        0 is good and 500 is very bad.

        @returns {float}

        @throws MissingValueException if the sensor was not calibrated before calling this
        method

        @throws MeasurementException if measuring failed
        """
        return _get_iaq_as_number(self._calc_iaq())

class MeasurementException(Exception):
    """
    Thrown if something went wrong with the measuring.
    """
    def __init__(self, message=None):
        """
        @param {str} (optional, default=None) message an error message to be added to this exception
        """
        super().__init__(message)

class MissingValueException(Exception):
    """
    Thrown when a value is None instead of an expected value.
    """
    def __init__(self, message=None):
        """
        @param {str} (optional, default=None) message an error message to be added to this exception
        """
        super().__init__(message)

def _get_iaq_as_number(score_from_calc_iaq) -> float:
    """
    Returns the indoor air quality (IAQ) score as a number as specified in the Bosch
    BME680 datasheet.

    @param {float} score_from_calc_iaq the value returned from a call to _calc_iaq

    @returns {float} the calculated indoor air quality index (IAQ)
    """
    return -1 if score_from_calc_iaq == -1 else round((100 - score_from_calc_iaq) * 5)

def _get_iaq_as_text(score_from_calc_iaq) -> str:
    """
    Gives the air quality as English text.

    @param {float} score_from_calc_iaq the value returned from a call to _calc_iaq

    @returns {str} the air quality as text

    @throws ValueError if an internal error happened which caused the indoor air quality
    values to be out of range 
    """
    iaq_score = _get_iaq_as_number(score_from_calc_iaq)

    if iaq_score == -1:
        return "Calibration needed"

    if iaq_score > 500 or iaq_score < -1:
        raise ValueError('Values are supposed to be in range [0, 500]')

    if (iaq_score >= 0 and iaq_score <= 50):
        return "Good"
    elif (iaq_score > 50 and iaq_score <= 100):
        return "Moderate"
    elif (iaq_score > 100 and iaq_score <= 150):
        return "Not so good"
    elif (iaq_score > 150 and iaq_score <= 200):
        return "Bad"
    elif (iaq_score > 200 and iaq_score <= 300):
        return "Worse than Bad"
    elif (iaq_score > 300 and iaq_score <= 500):
        return "Very bad"
    else:
        return "Unknown"
