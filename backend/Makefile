# Compiler and flags
CXX = g++
CXXFLAGS = -O3 -Wall -shared -std=c++17 -fPIC
DEBUGFLAGS = -g -Wall -shared -std=c++17 -fPIC

# Source and headers
SRC = pricing/black_scholes.cpp
HEADERS = pricing/black_scholes.h

# Output settings
OUT_DIR = build

# Platform detection
ifeq ($(OS),Windows_NT)
    EXT = dll
    RM = del /Q
    MKDIR = if not exist $(OUT_DIR) mkdir $(OUT_DIR)
else
    EXT = so
    RM = rm -f
    MKDIR = mkdir -p $(OUT_DIR)
endif

# Output file
OUT = $(OUT_DIR)/black_scholes.$(EXT)
DEBUG_OUT = $(OUT_DIR)/black_scholes_debug.$(EXT)

# Default target
all: $(OUT)

# Release build
$(OUT): $(SRC) $(HEADERS)
	$(MKDIR)
	$(CXX) $(CXXFLAGS) -o $@ $(SRC)

# Debug build
debug:
	$(MKDIR)
	$(CXX) $(DEBUGFLAGS) -o $(DEBUG_OUT) $(SRC)

# Clean build files
clean:
	@for %%f in (build\*.dll) do del "%%f"


# Force rebuild
rebuild: clean all
