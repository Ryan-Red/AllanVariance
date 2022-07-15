import matplotlib.pyplot as plt
import numpy as np
W_V_list = []





v_avg_list = []

fileName="accelTest.txt"
t, Ax, Ay, Az = np.loadtxt(fileName,unpack=True)

T = (t[-1] - t[0])#convert to seconds

N = len(Ax)


dt = T/N

print(dt)

field = ["Ax","Ay","Az"]

for j in range(0,3,1):

    name = field[j]
    print("Currently Processing {}".format(name))


    #Vx =  np.loadtxt(fileName,unpack=True)
    if name == "Ax":
        A = Ax[0:N]
    elif name == "Ay":
        A = Ay[0:N]
    else:
        A = Az[0:N]

    # spectral density calculation
    A_T = A/np.sqrt(T)
    A_f = np.fft.fft(A_T)*dt
    S_V = np.abs(A_f)**2


    f = np.fft.fftfreq(N,dt)
    W_V_list.append(2*S_V[f>0])   # keep only positive frequencies
    f = f[f>0]                    # keep only positive frequencies
    df = f[1]-f[0]
    # check that the fft function behaves properly, by verifying Parseval's theorem
    A_rms_time = np.std(A)

    #print("Time domain root-mean-squared = {}".format(V_rms_time) )
    #V_rms_freq = np.sqrt(np.trapz(W_V_list[i],x=f,dx=df))
    #print("Frequency domain root-mean-squared = {}".format(V_rms_freq))

    #Tot_avg_V_rms = Tot_avg_V_rms + (V_rms_time + V_rms_freq)/2


    # plot



    W_V_avg = np.mean(np.array(W_V_list),axis=0)
    A_rms_freq = np.sqrt(np.trapz(W_V_avg,x=f,dx=df))


    print("root-mean-squared from power spectrum = {} G".format(A_rms_freq))
    fig, ax = plt.subplots()

    Power = np.sqrt(W_V_avg)
    ax.loglog(f, Power, lw=2)
    ax.set_ylabel("Accel, $\sqrt{W_B}$ ")
    ax.set_xlabel("frequency, $f$ [Hz]")
    if name == "Ax":
        ax.set_title("Accel x vs Frequency $A_{x}$")
    elif name == "Ay":
        ax.set_title("Accel y vs Frequency $A_{y}$")
    else:
        ax.set_title("Accel z vs Frequency $A_{z}$")

    ax.margins(0,0.1)
    ax.grid()
    plt.show()

    saveFile = "accel_{}".format(name)

    plt.savefig(saveFile+".png")

    np.savetxt(saveFile+".txt",np.column_stack((f,Power)),delimiter="\t",header="frequency [Hz]\tMagnetic Field Spectrum")
