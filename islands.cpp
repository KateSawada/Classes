#include <stdlib.h>
#include <stdio.h>
/*
  島の数を数える問題
  地形は4x4のサイズで与えられる．
  #は陸を表し，-は海を表す．
  陸が上下左右に隣接している場合は，それを1つの島とみなす．
  斜めのみ繋がっている場合は別の島として数える．
  島がいくつあるか数えよ．
  例)

  #--#
  ###-
  ---#
  #-##  -> 4つ

  --##
  #--#
  ###-
  #--#  -> 3つ
  
*/
void checkNext(int x, int y, int *ary, int *checked){
    if (ary[(x + 1) + y * 4] == 1 && checked[(x + 1) + y * 4] == 0){
        checked[(x + 1) + y * 4] = 1;
        checkNext(x + 1, y, ary, checked);
    }
    if (ary[(x - 1) + y * 4] == 1 && checked[(x - 1) + y * 4] == 0){
        checked[(x - 1) + y * 4] = 1;
        checkNext(x - 1, y, ary, checked);
    }
    if (ary[x + (y + 1) * 4] == 1 && checked[x + (y + 1) * 4] == 0){
        checked[x + (y + 1) * 4] = 1;
        checkNext(x, y + 1, ary, checked);
    }
    if (ary[x + (y - 1) * 4] == 1 && checked[x + (y - 1) * 4] == 0){
        checked[x + (y - 1) * 4] = 1;
        checkNext(x, y - 1, ary, checked);
    }
}

int main(){
    int ans = 0;

    //entering the map
    char map1[256];
    char map2[256];
    char map3[256];
    char map4[256];
    printf("enter the map of row 1 with # and -\n");
    scanf("%s", map1);
    printf("enter the map of row 2 with # and -\n");
    scanf("%*c%s", map2);
    printf("enter the map of row 3 with # and -\n");
    scanf("%*c%s", map3);
    printf("enter the map of row 4 with # and -\n");
    scanf("%*c%s", map4);

    //converting char array to int array
    int ary[16];
    for (int i = 0; i < 4; i++){
        if (map1[i] == '#'){
            ary[i] = 1;
        } else if (map1[i] == '-'){
            ary[i] = 0;
        } else {
            printf("input character is wrong\n");
            exit(1);
        }
        if (map2[i] == '#'){
            ary[i + 4] = 1;
        } else if (map2[i] == '-'){
            ary[i + 4] = 0;
        } else {
            printf("input character is wrong\n");
            exit(1);
        }
        if (map3[i] == '#'){
            ary[i + 8] = 1;
        }else if (map3[i] == '-'){
            ary[i + 8] = 0;
        } else {
            printf("input character is wrong\n");
            exit(1);
        }
        if (map4[i] == '#'){
            ary[i + 12] = 1;
        } else if (map4[i] == '-'){
            ary[i + 12] = 0;
        } else {
            printf("input character is wrong\n");
            exit(1);
        }
    }

    //count islands
    int checked[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    for (int x = 0; x < 4; x++) {
        for (int y = 0; y < 4; y++){
            if (ary[x + y * 4] == 1 && checked[x + y * 4] == 0){
                checked[x + y * 4] = 1;
                checkNext(x, y, ary, checked);
                ans++;
            }
        }
    }

    //show answer
    printf("\n");
    printf("the map is\n");
    printf("%s\n", map1);
    printf("%s\n", map2);
    printf("%s\n", map3);
    printf("%s\n", map4);
    printf("there are %d islands\n", ans);

}
