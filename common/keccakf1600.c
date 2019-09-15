/* Based on the public domain implementation in
 * crypto_hash/keccakc512/simple/ from http://bench.cr.yp.to/supercop.html
 * by Ronny Van Keer
 * and the public domain "TweetFips202" implementation
 * from https://twitter.com/tweetfips202
 * by Gilles Van Assche, Daniel J. Bernstein, and Peter Schwabe */

#include <stdint.h>
#include <assert.h>
#include "keccakf1600.h"

#define NROUNDS 24
#define ROL(a, offset) ((a << offset) ^ (a >> (64-offset)))

/* static const uint64_t KeccakF_RoundConstants[NROUNDS] = */
/* { */
/*     (uint64_t)0x0000000000000001ULL, */
/*     (uint64_t)0x0000000000008082ULL, */
/*     (uint64_t)0x800000000000808aULL, */
/*     (uint64_t)0x8000000080008000ULL, */
/*     (uint64_t)0x000000000000808bULL, */
/*     (uint64_t)0x0000000080000001ULL, */
/*     (uint64_t)0x8000000080008081ULL, */
/*     (uint64_t)0x8000000000008009ULL, */
/*     (uint64_t)0x000000000000008aULL, */
/*     (uint64_t)0x0000000000000088ULL, */
/*     (uint64_t)0x0000000080008009ULL, */
/*     (uint64_t)0x000000008000000aULL, */
/*     (uint64_t)0x000000008000808bULL, */
/*     (uint64_t)0x800000000000008bULL, */
/*     (uint64_t)0x8000000000008089ULL, */
/*     (uint64_t)0x8000000000008003ULL, */
/*     (uint64_t)0x8000000000008002ULL, */
/*     (uint64_t)0x8000000000000080ULL, */
/*     (uint64_t)0x000000000000800aULL, */
/*     (uint64_t)0x800000008000000aULL, */
/*     (uint64_t)0x8000000080008081ULL, */
/*     (uint64_t)0x8000000000008080ULL, */
/*     (uint64_t)0x0000000080000001ULL, */
/*     (uint64_t)0x8000000080008008ULL */
/* }; */

void KeccakF1600_StateExtractBytes(uint64_t *state, unsigned char *data, unsigned int offset, unsigned int length)
{
    unsigned int i;
    for(i=0;i<length;i++)
    {
        data[i] = state[(offset + i) >> 3] >> (8*((offset + i) & 0x07));
    }
}

void KeccakF1600_StateXORBytes(uint64_t *state, const unsigned char *data, unsigned int offset, unsigned int length)
{
    unsigned int i;
    for(i = 0; i < length; i++)
    {
        state[(offset + i) >> 3] ^= (uint64_t)data[i] << (8 * ((offset + i) & 0x07));
    }
}

void keccakf1600(uint32_t* state);

void KeccakF1600_StatePermute(uint64_t * state)
{
  keccakf1600((uint32_t*)state);
}
