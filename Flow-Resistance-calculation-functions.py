import math

class InputData:
    diameter_in = 14/1000           # m
    diameter_out = 24 / 1000        # m
    length = 90/1000                # m
    flow_rate = 1*(1/1000/60)      # L/min

class Flow_Data:
    nu = 1.5*10**(-5) #m^2/s
    ro = 780 #kg/m^3
    mu =ro/nu

class Calculation:
    def __init__(self,length,flow_rate,dynamic_viscosity,density):
        self.l = length
        self.q = flow_rate
        self.ro = density
        self.nu = dynamic_viscosity

    @staticmethod
    def csa(d): return (math.pi * (d ** 2)) / 4

    def velocity(self,d): return self.q / Calculation.csa(d)  # velocity

    def re(self,d): return Calculation.velocity(self,d) * d / self.nu

    def friction_losses(self,d):
        l_range = 2000
        t_range = 4000
        lam = 64 / Calculation.re(self,d)
        turbu = 1 / (1.8 * math.log10(Calculation.re(self,d)) - 1.64) ** 2
        trans = (lam + ((lam - turbu) / l_range)) * Calculation.re(self,d) - l_range
        if Calculation.re(self,d) < l_range :
            kfr = lam
        elif  l_range < Calculation.re(self,d) < t_range:
            kfr = trans
        elif Calculation.re(self,d) > t_range:
            kfr = turbu
        return self.l * kfr * self.ro * (Calculation.velocity(self,d) ** 2) / 2 / d

    def inlet_outlet_losses (self, d, initialization):
           dpin = 0.5*self.ro*(Calculation.velocity(self,d)**2)/2
           dpout = self.ro * (Calculation.velocity(self,d) ** 2) / 2
           if initialization == "inlet": return dpin
           if initialization == "outlet": return dpout
           else: return print("inlet or outlet")

    def sudden_narrowing(self,d1,d2):
        return (self.ro*Calculation.velocity(self,d1)**2)\
               *((1 - (Calculation.csa(d1) / Calculation.csa(d2))) ** (3 / 4))

    def sudden_expansion(self,d1,d2):
        return 0.5*(self.ro * Calculation.velocity(self,d1) ** 2)\
               * ((1 - (Calculation.csa(d1) / Calculation.csa(d2))) **2)

    def turn(self,alf,d):
        return ((0.95*(math.sin(math.radians(alf/2)))**2)+2.05*(math.sin(math.radians(alf/2)))**4)\
               *0.5*self.ro*(Calculation.velocity(self,d)**2)



a = Calculation(InputData.length,InputData.flow_rate,Flow_Data.nu,Flow_Data.ro)

print(a.inlet_outlet_losses((InputData.diameter_in),"inlet"))
print(a.inlet_outlet_losses((InputData.diameter_in),"outlet"))
print(a.inlet_outlet_losses((InputData.diameter_out),"inlet"))
print(InputData.flow_rate)



