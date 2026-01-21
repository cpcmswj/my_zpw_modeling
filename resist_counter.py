import numpy as np
import jisuan_guidao as jg


class ResistCounter:
    def __init__(self,length_guidao,resist_per_meter,frequency):
        self.length_guidao=length_guidao
        self.resist_per_meter=resist_per_meter
        self.frequency=frequency
        self.angular_frequency=2*np.pi*frequency
    def get_resist_guidao(self):
        return self.length_guidao * self.resist_per_meter
    def get_resist_V1V2(self):
        """V1V2端即接收端输入变压器的输入阻抗"""
        if self.frequency==1700:
            return 36.0
        elif self.frequency==2000:
            return 43.2
        elif self.frequency==2300:
            return 48.6
        elif self.frequency==2600:
            return 55.0
        else:
            return 0
    def get_resist_cable(self):
        """电缆始端输入阻抗 Z_cd为电缆的特性阻抗 Z_d为电缆的特性阻抗"""
        Z_d=jg.find_SPTcable_parameters(self.frequency)[1]*np.exp(1j*jg.find_SPTcable_parameters(self.frequency)[2]*np.pi/180)
        Z_cd=50.0
        Z_V1V2=self.get_resist_V1V2()
        Z_R1=Z_cd*(Z_V1V2+Z_cd*np.tanh(Z_d))/(Z_V1V2*np.tanh(Z_d)+Z_cd)
        return Z_R1
    def get_resist_match(self):
        """接收端匹配单元入口端的阻抗"""
        Z_R2=
        return Z_R2
