#include "mbed.h"
#include "GPSReader.h"

Serial pcSerial(USBTX,USBRX,9600);

// char* storeLastSentence(char storeArray[67], char copiedArray[67])
// {
//     storeArray = copiedArray;
//     return storeArray;
// }

int main()
{
    GpsObject gpsObject;
    Timer t;
    float lastTime = 0;
    float timeInterwall = 1;
    //char dataToPc[60];
    //char lastKnownPlace[63];
    while(1)
    {
        t.start();
        gpsObject.getGPS();
        if(t.read() > lastTime + timeInterwall)
        {
            lastTime = t.read();
            if(gpsObject.getState() == 'A')
            {
                pcSerial.printf(" STATE = A ");
            }
            else if (gpsObject.getState() == 'V')
            {
                //tähän laskenta funktio uudelle paikalle...
                pcSerial.printf(" STATE = V!!! ");
            }
        }
        //pcSerial.printf(gpsObject.getOut(dataToPc));

        // pcSerial.printf(" %c ", dataToPc[0]);

        // else
        // {
            
        //     pcSerial.printf(" Virhe datassa. ");
        // }
    }
    return 0;
}

