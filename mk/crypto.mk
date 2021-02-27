SYMCRYPTO_SRC = \
	mupq/common/fips202.c \
	common/sha2.c \
	mupq/common/keccakf1600.c \
	mupq/pqclean/common/aes.c \
	mupq/common/sp800-185.c

obj/libsymcrypto.a: $(call objs,$(SYMCRYPTO_SRC))

obj/libsymcrypto-hashprof.a: CPPFLAGS+=-DPROFILE_HASHING
obj/libsymcrypto-hashprof.a: $(call hashprofobjs,$(SYMCRYPTO_SRC))

LDLIBS += -lsymcrypto$(if $(PROFILE_HASHING),-hashprof)
LIBDEPS += obj/libsymcrypto.a obj/libsymcrypto-hashprof.a
