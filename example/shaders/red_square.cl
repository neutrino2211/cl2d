__kernel void draw(__global uint8* buf, float elapsedTime, int width, int height) {
    int i = get_global_id(0);
    int j = get_global_id(1);
    int k = get_global_id(2);

    
    int colourFromId = (int) (i * (elapsedTime));
    int idx = (j * width) + i;
    int idy = i * j * 4;

    // if (j > 1) j = j - 400;
    // if (i > 1) i = i - 400;
    buf[0] = (char)0xff;
    buf[3] = (char)0xff;
    printf("I: %i, j: %i, k: %i, IDX: %i\n", i, j, k, idx);
}