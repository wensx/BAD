#!/usr/bin/python
import argparse
import matplotlib.pyplot as plt
import pandas as pd

fig, ((ax11, ax12), (ax21, ax22)) = plt.subplots(2, 2)

class Data:
    def __init__(self, filename):
        self.filename = filename
        self.data = {}
        self.times = {}

        i = 0
        for chunk in self.chunkYielder():
            dumpNumber, time, data = self.processChunk(chunk)
            self.data[i] = data
            self.times[i] = time
            i += 1

    def chunkYielder(self):
        lines = []
        with open(self.filename, 'r') as f:
            hasNIter = False
            hasTime = False
            hasHeaders = False
            
            # arf, not beautiful, should read it more carefully
            lines = [l.replace('\n', '') for l in f]

            i = 0

            while i < len(lines):
                niter = int(lines[i].split('#')[1])
                time = float(lines[i+1].split('#')[1])
                headers = lines[i+2].split('#')[1].split()
                data = []
                i += 3

                while i < len(lines) and '#' not in lines[i]:
                    data.append([float(val) for val in lines[i].split()])
                    i += 1
                yield niter, time, headers, data
                    
                    
                
                
    def processChunk(self, chunk):
        ''' Read the lines and get the following data in the lines:
        1: dump number
        2: time
        3: headers
        4+: data'''

        dumpNumber = chunk[0]
        time = chunk[1]
        headers = chunk[2]

        # read next line
        data = ([ [ float(el) for el in line] for line in chunk[3]])

        return dumpNumber, time, pd.DataFrame(data=data, columns=headers)

        


        
def plot(data):
    ax11.set_xdata(data['x'])
    ax11.set_ydata(data['T'])

    ax12.set_xdata(data['x'])
    ax12.set_ydata(data['S'])

    # ax21.set_xdata(data['x'])
    # ax21.set_xdata(data[''])

    ax22.set_xdata(data['T'])
    ax22.set_ydata(data['S'])

if __name__ == '__main__':
    print('Reading initial conditions')
    ic = pd.read_csv('CI.dat', delim_whitespace=True)
    
    print('Reading output file')
    data = Data('output.dat')

    print('Reading S curve')
    s_curve = pd.read_csv('critical_points/file.dat', delim_whitespace=True)

    x0 = data.data[1]

    ax11.set_xlabel('$x$')
    ax11.set_ylabel('$T^\star$')
    ax11.plot(ic['r'], ic['T'], label='Initial conditions')
    ax11.plot(x0['r'], x0['T'], label='Foobar')
    ax11.set_yscale('log')
    ax11.legend()
    
    ax12.set_xlabel('$r$')
    ax12.set_ylabel('$\Sigma$')
    ax12.plot(ic['r'], ic['Sigma'])
    ax12.plot(x0['r'], x0['Sigma'])
    ax12.set_yscale('log')

    ax22.set_xlabel('$\Sigma$')
    ax22.set_ylabel('$T$')
    
    ax22.plot(ic['Sigma'], ic['T'])
    ax22.plot(x0['Sigma'], x0['T'])
    ax22.plot(s_curve['sigma0'], s_curve['T0'], '--')
    ax22.set_yscale('log')
    ax22.set_xscale('log')

    plt.show()
