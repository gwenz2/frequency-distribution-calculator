#include<iostream>
#include<cmath>
#include <iomanip>
using namespace std;


int raw, i = 0, loop = 0, rTotal = 0; //for inputRaw
int hValue = -999, lValue = 999, store[999];

float R,C,K; //for gettingClasWidth
 
int lCi1, hCi1, freq = 0, cF, LcF, FTotal = 0; // for Processing
double lcB, hcB, cM, rFTotal = 0, rFTotal2=0;
int ii = 0, test = 0;
int arr = 0, arr2 = 1, arrNum = 0;
 
int cIntervals[2][99],  LcFrequency[99], GcFrequency[99];// for Displaying Table
float cBounderies[2][99], cMarks[99], rFrequency[99], rF[99], rFp[99], Frequency[99], LrFrequency[99], GrFrequency[99];
 
 
 void inputRaw() 
{
     while (loop != 1) 
    {
        cin >> raw;
        if (raw == 1000) 
             {
              cout << " ^ not a data!\n"; loop++; break;
             }
        else 
            { 
              store[i] = raw; 
              if (raw > hValue) hValue = raw; 
              if (raw < lValue) lValue = raw; 
              i++; rTotal = i;
            }
             
    }
}
        
void gettingClasWidth() 
{
    R = hValue - lValue;
    K = 1 + (33.0 / 10) * (log(rTotal) / log(10)); 
        K = ceil(K);
    C = R/K;
        C = ceil(C);
        
}        
        
void Processing ()
{
      while (hCi1 < hValue) 
    {
      if (test == 0) { lCi1 = lValue; hCi1 = lValue + (C-1); }
      else { lCi1+=C; hCi1+=C ;}
      cIntervals[arr][arrNum] = lCi1; cIntervals[arr2][arrNum] = hCi1;
    
      if (test == 0) {lcB = lCi1 - 0.5; hcB = hCi1 + 0.5;}
      else { lcB = lCi1 - 0.5; hcB = hCi1 + 0.5; }
      cBounderies[arr][arrNum] = lcB; cBounderies[arr2][arrNum] = hcB;
     
      if (test == 0) {cM = (lcB + hcB) / 2;}
      else {cM = (lcB + hcB) / 2;}
      cMarks[arrNum] = cM;
      
      freq = 0;
      for (ii = 0; ii < rTotal; ii++)
          { if (store[ii] >= lCi1 && store[ii] <= hCi1) freq++; }
      Frequency[arrNum] = freq;
      
      LcF += freq;
      LcFrequency[arrNum] = LcF;
      FTotal+=freq;
      
      ++arrNum; test++;
    }
    
    for (int i=0; i < arrNum; i++) 
    { 
        GcFrequency[i] = FTotal;
        FTotal-=Frequency[i]; 
        
        rF[i] = Frequency[i] / LcF;
        
        rFp[i] = (Frequency[i] / LcF) * 100;
        
        rFTotal += rFp[i];
        LrFrequency[i] = rFTotal;
        rFTotal2 += rFp[i];
    }
    
    for (int i = 0; i < arrNum; i++) 
    { 
        GrFrequency[i] = rFTotal2;
        rFTotal2 -= rFp[i]; 
    }   
}
    
void ClassIntervals() 
{
    for(int i = 0; i < arrNum; i++) {   
 cout << cIntervals[arr][i] << " - " << cIntervals[arr2][i] << endl; } 
}

void ClassBoundaries()
{
     for(int i = 0; i < arrNum; i++) {   
 cout << cBounderies[arr][i] << " - " << cBounderies[arr2][i] << endl; }
}
 
void ClassMarks() 
{
for(int i = 0; i < arrNum; i++) {   
 cout << cMarks[i] << endl; }
} 

void Frequency1()
{
for(int i = 0; i < arrNum; i++) {   
 cout << Frequency[i] << endl; }
}

void LcFrequency1()
{
for(int i = 0; i < arrNum; i++) {   
 cout << LcFrequency[i] << endl; }
}

void GcFrequency1()
{
for(int i = 0; i < arrNum; i++) {   
 cout << GcFrequency[i] << endl; }
}

void rFrequency1()
{
for(int i = 0; i < arrNum; i++) {   
 cout << fixed << setprecision(4) << rF[i] << " or "; 
 cout << fixed << setprecision(2) << rFp[i] << endl; }
}

void LrFrequency1()
{
for(int i = 0; i < arrNum; i++) {   
 cout << LrFrequency[i] << endl; }
}

void GrFrequency1() 
{
for(int i = 0; i < arrNum; i++) {   
 cout << GrFrequency[i] << endl; }
}


int main()
{
    cout << "Enter raw data (1000 to End)" << endl;
    inputRaw();
    
    gettingClasWidth();
    cout << "\n\n\nTotal raw data: " << rTotal <<
            "\nHighest Value: " << hValue << 
            "\nLowest Value: " << lValue <<
            "\nRange: " << R <<
            "\nClass Width: " << C;
    
    Processing();
    
    cout << "\n\nClass Intervals" << endl;   
    ClassIntervals();
 
    cout << "\n\nClass Boundaries" << endl;   
    ClassBoundaries();
 
    cout << "\n\nClass Marks" << endl;   
    ClassMarks();
 
    cout << "\n\nFrequency" << endl;   
    Frequency1();
    
    cout << "\n\n<cF" << endl;
    LcFrequency1();
    
    cout << "\n\n>cF" << endl;
    GcFrequency1();
    
    cout << "\n\nrF" << endl;
    rFrequency1();
    
    cout << "\n\n<rF" << endl;
    LrFrequency1();
    
    cout << "\n\n>rF" << endl;
    GrFrequency1();
}