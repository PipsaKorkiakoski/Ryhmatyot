#ifndef GPSREADER_H
#define GPSREADER_H

using namespace std;

class GpsObject
{
    public:
        explicit GpsObject();
        void getGPS();
        void modifyGPS();
        void getField(char*, int);
        float getLat();
        float getLong();
        char getNs();
        char getEw();
        char getState();
        float getSpeed();
        float getDirection();
        // char* getOut(char[60]);

    private:
        char output[67];
        // static const int sentenceSize = 70;
        // char sentence[70];
        char rmcLine[60];
        float speed;
        float latitude;
        float longitude;
        float direction;
        char state;
        char ew;
        char ns;
};

#endif