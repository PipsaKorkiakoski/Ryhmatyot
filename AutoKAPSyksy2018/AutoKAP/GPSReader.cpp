#include "mbed.h"
#include "GPSReader.h"
#include <RawSerial.h>
#include <string.h>
#include <string>

    Serial serial(USBTX,USBRX,9600);
    RawSerial gpsSerial(D14, D15,9600); // RX, TX (TX not used)
    // const int sentenceSize = 70;
    // char sentence[sentenceSize];
    const int outputSize = 60;
    char output[outputSize];
    // char ch;
    char field[20];
    char rmcLine[60];
    float speed = 0;
    float latitude = 0;
    char ns = ' ';
    float longitude = 0;
    char ew = ' ';
    float direction = 0;
    char state = ' ';

    GpsObject::GpsObject()
    {

    }

    void GpsObject::getGPS()
    {
        if (gpsSerial.readable() && gpsSerial.getc() == '$')
        {
            static int i = 0;
            if(gpsSerial.getc() == 'G')
            {
                if(gpsSerial.getc() == 'P')
                {
                    if(gpsSerial.getc() == 'R')
                    {
                        if(gpsSerial.getc() == 'M')
                        {
                            if(gpsSerial.getc() == 'C')
                            {
                                if(gpsSerial.getc() == ',')
                                {
                                    while(i < 59)
                                    {
                                    rmcLine[i] = gpsSerial.getc();
                                    i++;
                                    }
                                    rmcLine[i] = '\n';
                                    modifyGPS();
                                    serial.printf(output);
                                }
                            }
                        }
                    }
                }
            }
            i = 0;
        }


        // if (gpsSerial.readable())
        // {
        //     int i = 0;
        //     while(i < sentenceSize)
        //     {
        //         ch = gpsSerial.getc();
        //         //serial.printf("%c", ch);
        //         if (ch != '\n' && i < sentenceSize)
        //         {
        //             sentence[i] = ch;
        //             i++;
        //         }
        //         else
        //         {
        //             sentence[i+1] = '\0';
        //             i = 70;
        //         }
        //     }
        //     modifyGPS();
        // }
    }

    void GpsObject::modifyGPS()
    {
        memset(output, 0, outputSize * (sizeof output[0]) );
        getField(field, 1); //state: 'A' = active, 'V' = void
        strcat(output,field);
        state = field[0];
        strcat(output," Lat: ");
        getField(field, 2);  // number
        strcat(output,field);
        latitude = std::atof(field);
        getField(field, 3); // N/S
        strcat(output,field);
        ns = field[0];
        strcat(output," Long: ");
        getField(field, 4);  // number
        strcat(output,field);
        longitude = std::atof(field);
        getField(field, 5);  // E/W
        strcat(output,field);
        ew = field[0];
        strcat(output," Speed: ");
        getField(field, 6); //speed in knots
        speed = std::atof(field) * 0.514444444;
        char spd[4];
        snprintf(spd,4,"%f", speed);
        strcat(output,spd);
        strcat(output," Direction: ");
        getField(field, 7);
        strcat(output,field);
        direction = atof(field);
    }

    float GpsObject::getLat()
    {
        return latitude;
    }

    float GpsObject::getLong()
    {
        return longitude;
    }

    float GpsObject::getSpeed()
    {
        return speed;
    }

    float GpsObject::getDirection()
    {
        return direction;
    }

    char GpsObject::getEw()
    {
        return ew;
    }

    char GpsObject::getNs()
    {
        return ns;
    }

    char GpsObject::getState()
    {
        return state;
    }

    // char* GpsObject::getOut(char array[outputSize])
    // {
    //     getGPS();
    //     array = rmcLine;
    //     return array;
    // }

    void GpsObject::getField(char* buffer, int index)
    {
        int linePos = 0;
        int fieldPos = 0;
        int commaCount = 0;
        while (linePos < 60)
        {
            if (rmcLine[linePos] == ',')
            {
                commaCount ++;
            }
            if (commaCount == index && rmcLine[linePos] != ',')
            {
                buffer[fieldPos] = rmcLine[linePos];
                fieldPos ++;
            }
            linePos ++;
        }
        buffer[fieldPos] = '\0';
    } 