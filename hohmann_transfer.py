import math
mu = 1.33*10**(20) #G*Mdot
r_earth=1.5*10**(11) #distance of Earth from the sun
r_jupiter = 5.2*1.5*10**(11) #distance of Jupiter from the sun
e=0.25 #eccentricity of pluto
a=39.45*1.5*10**(11) #semi major axis of pluto
c_ma = 319.4 #current mean anomoly of pluto


def circular_circular(rp,ra):
    '''Given an rp and ra (or distance from the sun of orgin circular orbit and target circular orbit) it will return the two delta v's needed'''
    a = (rp+ra)/2
    dv1 = math.sqrt(mu*ra/(rp*a))- v_circular(rp)
    dv2 = v_circular(ra) - math.sqrt(mu*rp/(ra*a))
    return dv1,dv2

def v_circular(r):
    '''The velocity of a circular orbit at a distance from the sun'''
    return math.sqrt(mu/r)

def circular_eliptical(r,e,a,return_='dv1,dv2'):
    ''''The delta v (or other parameters, passed as strings to return_) for a hohmann transfer between a circular body at distance r fron the sun and an eliptical body with semi major axis a and eccentricity e'''
    a_o = a 
    rp_h = r
    rp_o = a*(1-e)
    ra_o = a*(1+e)
    ra_h = ra_o
    a_h = (rp_h+ra_h)/2
    a = a_h
    dv1 = math.sqrt(mu*ra_h/(rp_h*a_h))- v_circular(rp_h) #v_p (hohmann) - v_c (earth)
    dv2 = math.sqrt((mu*rp_o)/(a_o*ra_o)) - math.sqrt(mu*rp_h/(ra_h*a_h)) #v_a (target) - v_a (hohmann)
    return(eval(return_)) #hackey solution to avoid class instances and kwargs 

def get_period(a):
    '''Given a semi major axis in meters, it returns the orbital period in days using Kepler's 3rd law'''
    return ((a/(1.5*10**(11)))**3)**(1/2)*365

def optimal_launch_deg(r_orgin,e,a,ma):
    '''Given the same parameters as circular_eliptical, it calculates the optimal launch window in days in the future (since March 30, 2020) and the mean anomoly of Pluto at launch'''
    a_o,a_h = circular_eliptical(r_orgin,e,a,'a_o,a_h')
    p_h = get_period(a_h)/2 #half period of hohmann
    p_o = get_period(a_o) #period of destination
    deg_moved_transfer = (360/p_o)*p_h
    when_pluto_at_180 = (ma-180)/(360/p_o)
    when_leave = when_pluto_at_180 - p_h #days until launch
    deg_leave = 180 - deg_moved_transfer #mean anomoly of pluto at launch
    return when_leave, deg_leave

dv1,dv2 = circular_circular(r_earth,r_jupiter) #Earth to Jupiter
dv1,dv2 = circular_eliptical(r_earth,e,a) #Earth to Pluto
days_until_launch,mean_anomoly_launch = optimal_launch_deg(r_earth,e,a,c_ma)
