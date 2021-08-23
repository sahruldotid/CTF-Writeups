#include <stdio.h>
#include <math.h>
#include <string.h>

// gcc loop.c -o loop -lm

int is_prime(int a1){
  int i;
  if ( a1 <= 1 )
    return 0;
  for ( i = 2; i <= sqrt(a1); ++i )
  {
    if ( !(a1 % i) )
      return 0;
  }
  return 1;
}



int main(int argc, char const *argv[])
{
	char flag[] = "ujp?_oHy_lxiu_zx_uve";
	int v6;
	for ( int i = 0; i < strlen(flag); ++i ){
	    v6 = 4 * i;
	    for ( int j = is_prime(4 * i); j != 1; j = is_prime(v6) )
	      ++v6;
	  	printf("%d ", v6);	    
	}
}