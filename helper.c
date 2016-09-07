#include <stdio.h>
#include <stdlib.h>

int main(void)
{
	int c;
	FILE * fp_wt = fopen("index.html", "r");
	FILE * fp_nt = fopen("index_notab.html", "w");
	
	while((c=fgetc(fp_wt))!=EOF){
		if ( '\t' == (char) c){
			fputc(' ',fp_nt); fputc(' ', fp_nt);
			continue;
		}
		fputc(c, fp_nt);
	}

	fclose(fp_nt);
	fclose(fp_wt);
	
	return 0;
}