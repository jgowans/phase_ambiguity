#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import scipy.constants

def generate_rho(psi):
    """ Not really ranges. Lists of values to compute for.
    If you have the edges, for a colourmesh:
    edge = np.linspace(0, 100, 1000)
    mid = [(edge[i+1]+edge[i])/2 for i in range(len(edge)-1)]
    """
    #k = 15      # dielectric constant
    k = 5      # dielectric constant
    alpha = 10e-2   # conductivity
    alpha = 0.10   # conductivity
    omega = 250e6 * 2*np.pi
    #omega = (scipy.constants.c / 0.09) * 2*np.pi

    chi = alpha/(omega*scipy.constants.epsilon_0)
    rho = (
        (((k - (1j * chi))*np.sin(psi)) - np.sqrt((k - (1j*chi))-np.square(np.cos(psi)))) /
        (((k - (1j * chi))*np.sin(psi)) + np.sqrt((k - (1j*chi))-np.square(np.cos(psi))))
    )
    return rho

def generate_d_h_rho_colourmesh():
    d_edge = np.linspace(0, 50, 1000, endpoint = False)
    d_mid = [(d_edge[i+1]+d_edge[i])/2 for i in range(len(d_edge)-1)]
    h_edge = np.linspace(0.1, 5, 200, endpoint = False)
    h_mid = [(h_edge[i+1]+h_edge[i])/2 for i in range(len(h_edge)-1)]

    psi = np.linspace(0, np.radians(90), 1000)
    plt.plot(np.degrees(psi),np.angle( generate_rho(psi)))
    plt.plot(np.degrees(psi),np.abs( generate_rho(psi)))
    plt.show()

    Z = np.ndarray((len(d_mid), len(h_mid)), dtype=np.complex128)
    for idx, d in enumerate(d_mid):
        # d/2 because reflection occurs midway the distance between the antennas
        psi = np.arctan2(h_mid, d/2)
        Z[idx] = generate_rho(psi)
    X, Y = np.meshgrid(d_mid, h_mid)
    Z = Z.T
    plt.pcolormesh(X, Y, np.angle(Z))
    plt.colorbar()
    plt.show()
    plt.pcolormesh(X, Y, np.abs(Z))
    plt.colorbar()
    plt.show()

def from_thomas():
    h=3   # source antenna height
    maxrange=40.0  # maximum range
    freq=250.0  # MHz
    xx=(30.0-1)/.05;

    wavelength=300/freq

    x=np.array([np.arange(1,maxrange,0.05)]);
    y=np.array([np.arange(0,5,0.05)]).T
    allx=np.dot(np.array([np.ones(np.shape(y)[0])]).T,x)
    ally=np.dot(y,np.array([np.ones(np.shape(x)[1])]))

    range1=np.sqrt(allx**2.0+(ally-h)**2.0)
    range2=np.sqrt(allx**2.0+(ally+h)**2.0)

    angle1=np.arctan2(ally-h,allx)
    angle2=np.arctan2(ally+h,allx)

    # far fields are, crudely: (ground reflection coefficient) * (antenna pattern, assume cosine) * (1/r) * (e^-j beta x)
    signal1 = 1.0*np.cos(angle1)/range1 * np.exp(np.complex(0,-2.0*np.pi/wavelength)*range1)
    signal2 = 0.71*np.cos(angle2)/range2 * np.exp(np.complex(0,-2.0*np.pi/wavelength)*range2)

    signal=signal1+signal2;

    fig0 = plt.figure(figsize=(16,4))
    plt.pcolor(x,y,20*np.log10(np.abs(signal)))
    plt.plot([0,0,0],[h-wavelength/4.0,h,h+wavelength/4.0],lw=2,marker='s',color='k')
    plt.plot([-1,maxrange],[0,0],lw=1,color='k')
    plt.plot([x[0,xx],x[0,xx]],[0,5],lw=2,color='w',linestyle='--')
    plt.colorbar(); plt.grid(True)
    plt.clim([-30,0]);  plt.xlim([-1,maxrange]);  plt.ylim([0,5]);  
    plt.ylabel('Height above ground, m');  plt.xlabel('Distance from source, m');
    plt.title('Far fields of a dipole %3.1f m above ground, dBVolts' % h)

    fig1 = plt.figure(figsize=(16,4))
    plt.pcolor(x,y,np.angle(signal),cmap=plt.get_cmap('hsv'))
    plt.plot([0,0,0],[h-wavelength/4.0,h,h+wavelength/4.0],lw=2,marker='s',color='k')
    plt.colorbar(); plt.grid(True);  plt.clim([-np.pi,np.pi]);  plt.xlim([-1,maxrange]);  plt.ylim([0,5]);
    plt.ylabel('Height above ground, m');  plt.xlabel('Distance from source, m');
    plt.title('Far field phases of a dipole %3.1f m above ground, dBVolts' % h)

    f, (ax1, ax2, ax3) = plt.subplots(1,3,sharey=True,figsize=(12,3.5))
    mag=20*np.log10(np.abs(signal[:,xx]));
    ax1.plot(mag-mag[0],y);
    mag2=20*np.log10(np.abs(signal[:,xx+10]));
    ax1.plot(mag2-mag[0],y);
    ax1.set_xlim([-6,0]); ax1.set_ylim([0,5]); ax1.grid(True);
    ax1.set_xlabel('E field magnitude, dBVolts, normalised to y=0');  ax1.set_ylabel('Height above ground, m');
    ax1.set_title('Elevation cut x=%5.0f m away. Source at %3.1f m' % (x[0,xx],h));

    ph=np.unwrap(np.angle(signal[:,xx]));
    ax2.plot(ph-ph[0],y)
    ph2=np.unwrap(np.angle(signal[:,xx+10]));
    ax2.plot(ph2-ph[0],y)
    ax2.set_xlabel('(Unwrapped) Phase, radians');
    ax2.grid(True);  ax2.set_ylim([0,5]);   #ax2.set_xlim([-1.8,1])
    ax2.set_title('Elevation cut x=%5.0f m away. Source at %3.1f m' % (x[0,xx],h));

    ph3=np.unwrap(np.angle(signal[:,xx+10]));
    ax3.plot(ph-ph2,y)
    ax3.set_xlabel('(Unwrapped) Phase difference, radians');
    ax3.grid(True);  ax3.set_ylim([0,5]);   #ax3.set_xlim([-1.8,1])
    ax3.set_title('Elevation cut x=%5.0f m away. Source at %3.1f m' % (x[0,xx],h));

    plt.show()
