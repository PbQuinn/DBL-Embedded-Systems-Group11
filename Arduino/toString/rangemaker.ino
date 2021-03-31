// make ranges in which we can sense objects 
// if the difference is not significant we want need new readings
boolean rangemaker(int lowest, int highest, int arrayrange[]) {
  int difference = (highest - lowest);
  if (difference < 20) {
    return false;
  } else {
    if (difference >= 40){
      arrayrange[0] = lowest - 20;
      arrayrange[1] = lowest + 20;
      arrayrange[2] = highest - 20;
      arrayrange[3] = highest  + 20;
    } else {
      arrayrange[0] = lowest - 10;
      arrayrange[1] = lowest + 10;
      arrayrange[2] = highest - 10;
      arrayrange[3] = highest  + 10;
    }
       
    return true;
  }


}
