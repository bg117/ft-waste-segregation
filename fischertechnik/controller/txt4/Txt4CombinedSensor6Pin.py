import smbus2
from ..CombinedSensor import CombinedSensor

class ICM_42670_P(object):
    GYRO_ACC_ADDR = 0x68

    GYRO_ACC_PWR_MGMT0_ADDR = 0x1F
    GYRO_ACC_PWR_MGMT0_BITMASK = 0b00001111
    PowerMode = {
        'Sleep': 0b0000,  # Gyroscope: OFF, Accelerometer: OFF
        'Standby': 0b0100,  # Gyroscope: DRIVE ON, Accelerometer: OFF
        'AccelLowPower': 0b0010,  # Gyroscope: OFF, Accelerometer: DUTY - CYCLED
        'AccelLowNoise': 0b0011,  # Gyroscope: OFF, Accelerometer: ON
        'GyroLowNoise': 0b1100,  # Gyroscope: ON, Accelerometer: OFF
        'SixAxisLowNoise': 0b1111  # Gyroscope: ON, Accelerometer: ON
    }

    GYRO_CONFIG0_ADDR = 0x20
    ACC_CONFIG0_ADDR = 0x21

    GYRO_CONFIG0_RANGE_BITMASK = 0b01100000
    GYRO_CONFIG0_ODR_BITMASK = 0b00001111
    GYRO_CONFIG0_BITMASK = GYRO_CONFIG0_RANGE_BITMASK | GYRO_CONFIG0_ODR_BITMASK

    ACC_CONFIG0_RANGE_BITMASK = 0b01100000
    ACC_CONFIG0_ODR_BITMASK = 0b00001111
    ACC_CONFIG0_BITMASK = ACC_CONFIG0_RANGE_BITMASK | ACC_CONFIG0_ODR_BITMASK

    GYRO_CONFIG1_ADDR = 0x23
    ACC_CONFIG1_ADDR = 0x24

    GYRO_CONFIG1_BITMASK = 0b00000111

    ACC_CONFIG1_AVG_FILTER_BITMASK = 0b01110000
    ACC_CONFIG1_LOWPASS_FILTER_BITMASK = 0b00000111
    ACC_CONFIG1_BITMASK = ACC_CONFIG1_AVG_FILTER_BITMASK | ACC_CONFIG1_LOWPASS_FILTER_BITMASK

    GYRO_X_MSB = 0x11
    GYRO_X_LSB = 0x12
    GYRO_Y_MSB = 0x13
    GYRO_Y_LSB = 0x14
    GYRO_Z_MSB = 0x15
    GYRO_Z_LSB = 0x16

    ACC_X_MSB = 0x0B
    ACC_X_LSB = 0x0C
    ACC_Y_MSB = 0x0D
    ACC_Y_LSB = 0x0E
    ACC_Z_MSB = 0x0F
    ACC_Z_LSB = 0x0E

    GyroRange = {
        250: 131.0,
        500: 65.5,
        1000: 32.8,
        2000: 16.4
    }

    GyroRangeBits = {
        250: 0b01100000,
        500: 0b01000000,
        1000: 0b00100000,
        2000: 0b00000000
    }

    AccRange = {
        2: 16384.0,
        4: 8192.0,
        8: 4096.0,
        16: 2048.0
    }

    AccRangeBits = {
        2: 0b01100000,
        4: 0b01000000,
        8: 0b00100000,
        16: 0b00000000
    }

    AccOdrBits = {
        1600: 0b0101,
        800: 0b0110,
        400: 0b0111,
        200: 0b1000,
        100: 0b1001,
        50: 0b1010,
        25: 0b1011,
        12.5: 0b1100,
        6.25: 0b1101,
        3.125: 0b1110,
        1.5625: 0b1111
    }

    GyroOdrBits = {
        1600: 0b0101,
        800: 0b0110,
        400: 0b0111,
        200: 0b1000,
        100: 0b1001,
        50: 0b1010,
        25: 0b1011,
        12.5: 0b1100,
    }

    GyroLowPassFilterBits = {
        0: 0b0000,
        180: 0b0001,
        121: 0b0010,
        73: 0b0011,
        53: 0b0100,
        34: 0b0101,
        25: 0b0110,
        16: 0b0111
    }

    AccLowPassFilterBits = {
        0: 0b0000,
        180: 0b0001,
        121: 0b0010,
        73: 0b0011,
        53: 0b0100,
        34: 0b0101,
        25: 0b0110,
        16: 0b0111
    }

    AccAverageFilterBits = {
        2: 0b0000,
        4: 0b0001,
        8: 0b0010,
        16: 0b0011,
        32: 0b0100,
        64: 0b0101,
    }

class MMC5603NJ(object):
    MAGNETOMETER_ADDRESS = 0x30

    MMC56X3_PRODUCT_ID = 0x39
    MMC56X3_CTRL0_REG = 0x1B
    MMC56X3_CTRL1_REG = 0x1C
    MMC56X3_CTRL2_REG = 0x1D
    MMC56X3_STATUS_REG = 0x18
    MMC56X3_OUT_TEMP = 0x09
    MMC56X3_OUT_X_L = 0x00
    MMC5603_ODR_REG = 0x1A

    MAG_Xout_0 = 0x00
    MAG_Xout_1 = 0x01
    MAG_Yout_0 = 0x02
    MAG_Yout_1 = 0x03
    MAG_Zout_0 = 0x04
    MAG_Zout_1 = 0x05
    MAG_Xout_2 = 0x06
    MAG_Yout_2 = 0x07
    MAG_Zout_2 = 0x08


class Txt4CombinedSensor6Pin(CombinedSensor):
    def __init__(self, controller, identifier):
        CombinedSensor.__init__(self, controller, identifier)
        self.__gyro_resolution = 0
        self.__acc_resolution = 0
        self.__i2c = smbus2.SMBus(3)
        self.__is_accelerometer_initialized = False
        self.__is_magnetometer_initialized = False
        self.__is_gyrometer_initialized = False
        self.set_power_mode(ICM_42670_P.PowerMode['SixAxisLowNoise'])

    def set_power_mode(self, mode=ICM_42670_P.PowerMode['SixAxisLowNoise']):
        self.update_reg(ICM_42670_P.GYRO_ACC_ADDR, ICM_42670_P.GYRO_ACC_PWR_MGMT0_ADDR,
                        mode,
                        ICM_42670_P.GYRO_ACC_PWR_MGMT0_BITMASK)

    def read_power_mode(self):
        result = self.__i2c.read_byte_data(ICM_42670_P.GYRO_ACC_ADDR,
                                           ICM_42670_P.GYRO_ACC_PWR_MGMT0_ADDR) & ICM_42670_P.GYRO_ACC_PWR_MGMT0_BITMASK
        return [k for k, v in ICM_42670_P.PowerMode.items() if v == result][0]

    def init_accelerometer(self, acc_range=16, odr=800):
        self.__acc_resolution = 1 / ICM_42670_P.AccRange[acc_range]
        self.update_reg(ICM_42670_P.GYRO_ACC_ADDR, ICM_42670_P.ACC_CONFIG0_ADDR,
                        ICM_42670_P.AccRangeBits[acc_range] | ICM_42670_P.AccOdrBits[odr],
                        ICM_42670_P.ACC_CONFIG0_BITMASK)
        self.__is_accelerometer_initialized = True

    def init_gyrometer(self, gyro_range=2000, odr=800):
        self.__gyro_resolution = 1 / ICM_42670_P.GyroRange[gyro_range]
        self.update_reg(ICM_42670_P.GYRO_ACC_ADDR, ICM_42670_P.GYRO_CONFIG0_ADDR,
                        ICM_42670_P.GyroRangeBits[gyro_range] | ICM_42670_P.GyroOdrBits[odr],
                        ICM_42670_P.GYRO_CONFIG0_BITMASK)
        self.__is_gyrometer_initialized = True

    def init_magnetometer(self, odr=255):
        if not ((odr == 1000) or (0 <= odr <= 255)):
            raise ValueError('Data rate must be 0-255 or 1000 Hz!')
        mag_ctrl2_cache = self.__i2c.read_byte_data(MMC5603NJ.MAGNETOMETER_ADDRESS, MMC5603NJ.MMC56X3_CTRL2_REG)
        if odr == 1000:
            self.__i2c.write_byte_data(MMC5603NJ.MAGNETOMETER_ADDRESS, MMC5603NJ.MMC5603_ODR_REG, 255)
            mag_ctrl2_cache |= 0x80
        else:
            self.__i2c.write_byte_data(MMC5603NJ.MAGNETOMETER_ADDRESS, MMC5603NJ.MMC5603_ODR_REG, odr)
            mag_ctrl2_cache &= ~0x80
        self.__i2c.write_byte_data(MMC5603NJ.MAGNETOMETER_ADDRESS, MMC5603NJ.MMC56X3_CTRL2_REG, mag_ctrl2_cache)
        self.__is_magnetometer_initialized = True

    def get_acceleration_x(self) -> float:
        """
        Returns the current acceleration in X direction in g. 1g = 9.81m/s^2.
        @returns {float} acceleration in X direction in g
        """
        if self.__is_accelerometer_initialized:
            """
            On reading multiple bytes from i2c the register will be incremented.
            Therefore the lower register value will be read which is the MSB.
            The returned value is the most significant byte (MSB) and least significant byte (LSB) in reverse order.
            """
            result = self.__i2c.read_word_data(ICM_42670_P.GYRO_ACC_ADDR, ICM_42670_P.ACC_X_MSB)
            result = result.from_bytes(result.to_bytes(2, byteorder='big'), byteorder='little', signed='True')
            return result * self.__acc_resolution
        return None

    def get_acceleration_y(self) -> float:
        """
        Returns the current acceleration in X direction in g. 1g = 9.81m/s^2.
        @returns {float} acceleration in X direction in g
        """
        if self.__is_accelerometer_initialized:
            """
            On reading multiple bytes from i2c the register will be incremented.
            Therefore the lower register value will be read which is the MSB.
            The returned value is the most significant byte (MSB) and least significant byte (LSB) in reverse order.
            """
            result = self.__i2c.read_word_data(ICM_42670_P.GYRO_ACC_ADDR, ICM_42670_P.ACC_Y_MSB)
            result = result.from_bytes(result.to_bytes(2, byteorder='big'), byteorder='little', signed='True')
            return result * self.__acc_resolution
        return None

    def get_acceleration_z(self) -> float:
        """
        Returns the current acceleration in X direction in g. 1g = 9.81m/s^2.
        @returns {float} acceleration in X direction in g
        """
        if self.__is_accelerometer_initialized:
            """
            On reading multiple bytes from i2c the register will be incremented.
            Therefore the lower register value will be read which is the MSB.
            The returned value is the most significant byte (MSB) and least significant byte (LSB) in reverse order.
            """
            result = self.__i2c.read_word_data(ICM_42670_P.GYRO_ACC_ADDR, ICM_42670_P.ACC_Z_MSB)
            result = result.from_bytes(result.to_bytes(2, byteorder='big'), byteorder='little', signed='True')
            return result * self.__acc_resolution
        return None

    def get_rotation_x(self) -> float:
        """
        Returns the rotation speed around the X axis in degrees per second.
        @returns {float} rotation speed around the X axis in degrees per second
        """
        if self.__is_gyrometer_initialized:
            """
            On reading multiple bytes from i2c the register will be incremented.
            Therefore the lower register value will be read which is the MSB.
            The returned value is the most significant byte (MSB) and least significant byte (LSB) in reverse order.
            """
            result = self.__i2c.read_word_data(ICM_42670_P.GYRO_ACC_ADDR, ICM_42670_P.GYRO_X_MSB)
            result = result.from_bytes(result.to_bytes(2, byteorder='big'), byteorder='little', signed='True')
            return result * self.__gyro_resolution
        return None

    def get_rotation_y(self) -> float:
        """
        Returns the rotation speed around the X axis in degrees per second.
        @returns {float} rotation speed around the X axis in degrees per second
        """
        if self.__is_gyrometer_initialized:
            """
            On reading multiple bytes from i2c the register will be incremented.
            Therefore the lower register value will be read which is the MSB.
            The returned value is the most significant byte (MSB) and least significant byte (LSB) in reverse order.
            """
            result = self.__i2c.read_word_data(ICM_42670_P.GYRO_ACC_ADDR, ICM_42670_P.GYRO_Y_MSB)
            result = result.from_bytes(result.to_bytes(2, byteorder='big'), byteorder='little', signed='True')
            return result * self.__gyro_resolution
        return None

    def get_rotation_z(self) -> float:
        """
        Returns the rotation speed around the X axis in degrees per second.
        @returns {float} rotation speed around the X axis in degrees per second
        """
        if self.__is_gyrometer_initialized:
            """
            On reading multiple bytes from i2c the register will be incremented.
            Therefore the lower register value will be read which is the MSB.
            The returned value is the most significant byte (MSB) and least significant byte (LSB) in reverse order.
            """
            result = self.__i2c.read_word_data(ICM_42670_P.GYRO_ACC_ADDR, ICM_42670_P.GYRO_Z_MSB)
            result = result.from_bytes(result.to_bytes(2, byteorder='big'), byteorder='little', signed='True')
            return result * self.__gyro_resolution
        return None

    def get_magnetic_field_x(self) -> float:
        """
        Returns the current magnetic flux density in X direction in microtesla.
        @returns {float} mangnetic flux density in X direction in microtesla
        """
        if self.__is_magnetometer_initialized:
            Xout0 = self.__i2c.read_byte_data(MMC5603NJ.MAGNETOMETER_ADDRESS, MMC5603NJ.MAG_Xout_0) << 12
            Xout1 = self.__i2c.read_byte_data(MMC5603NJ.MAGNETOMETER_ADDRESS, MMC5603NJ.MAG_Xout_1) << 4
            Xout2 = self.__i2c.read_byte_data(MMC5603NJ.MAGNETOMETER_ADDRESS, MMC5603NJ.MAG_Xout_2) >> 4
            x = Xout0 | Xout1 | Xout2
            x -= 1 << 19
            x *= 0.00625
            # trigger next conversion
            self.__i2c.write_byte_data(MMC5603NJ.MAGNETOMETER_ADDRESS, 0x1B, 0x21)
            return x
        return None

    def get_magnetic_field_y(self) -> float:
        """
        Returns the current magnetic flux density in y direction in microtesla.
        @returns {float} mangnetic flux density in y direction in microtesla
        """
        if self.__is_magnetometer_initialized:
            Yout0 = self.__i2c.read_byte_data(MMC5603NJ.MAGNETOMETER_ADDRESS, MMC5603NJ.MAG_Yout_0) << 12
            Yout1 = self.__i2c.read_byte_data(MMC5603NJ.MAGNETOMETER_ADDRESS, MMC5603NJ.MAG_Yout_1) << 4
            Yout2 = self.__i2c.read_byte_data(MMC5603NJ.MAGNETOMETER_ADDRESS, MMC5603NJ.MAG_Yout_2) >> 4
            y = Yout0 | Yout1 | Yout2
            y -= 1 << 19
            y *= 0.00625
            # trigger next conversion
            self.__i2c.write_byte_data(MMC5603NJ.MAGNETOMETER_ADDRESS, 0x1B, 0x21)
            return y
        return None

    def get_magnetic_field_z(self) -> float:
        """
        Returns the current magnetic flux density in z direction in microtesla.
        @returns {float} mangnetic flux density in z direction in microtesla
        """
        if self.__is_magnetometer_initialized:
            Zout0 = self.__i2c.read_byte_data(MMC5603NJ.MAGNETOMETER_ADDRESS, MMC5603NJ.MAG_Zout_0) << 12
            Zout1 = self.__i2c.read_byte_data(MMC5603NJ.MAGNETOMETER_ADDRESS, MMC5603NJ.MAG_Zout_1) << 4
            Zout2 = self.__i2c.read_byte_data(MMC5603NJ.MAGNETOMETER_ADDRESS, MMC5603NJ.MAG_Zout_2) >> 4
            z = Zout0 | Zout1 | Zout2
            z -= 1 << 19
            z *= 0.00625
            # trigger next conversion
            self.__i2c.write_byte_data(MMC5603NJ.MAGNETOMETER_ADDRESS, 0x1B, 0x21)
            return z
        return None

    def update_reg(self, address, register, value, mask):
        current = self.__i2c.read_word_data(address, register)
        val = (current & ~mask) | (value & mask)
        self.__i2c.write_byte_data(address, register, val)
