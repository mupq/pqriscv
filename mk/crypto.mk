SYMCRYPTO_SRC = \
	mupq/common/fips202.c \
	mupq/common/sp800-185.c \
	mupq/common/nistseedexpander.c \
	common/sha2.c \
	mupq/common/keccakf1600.c \
	mupq/pqclean/common/aes.c

obj/libsymcrypto.a: $(call objs,$(SYMCRYPTO_SRC))

obj/libsymcrypto-hashprof.a: CPPFLAGS+=-DPROFILE_HASHING
obj/libsymcrypto-hashprof.a: $(call hashprofobjs,$(SYMCRYPTO_SRC))

ifeq ($(AIO),1)
LDLIBS +=
LIBDEPS += $(SYMCRYPTO_SRC)
CPPFLAGS+=$(if $(PROFILE_HASHING),-DPROFILE_HASHING)
else
LDLIBS += -lsymcrypto$(if $(PROFILE_HASHING),-hashprof)
LIBDEPS += obj/libsymcrypto$$(if $$(PROFILE_HASHING),-hashprof).a
endif
