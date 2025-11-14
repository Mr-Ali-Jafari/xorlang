# Directories
SRC   := src
BUILD := build

# Files
EXEC    := xorlang
SOURCES := $(wildcard $(SRC)/*.c)
OBJECTS := $(patsubst $(SRC)/%.c, $(BUILD)/%.o, $(SOURCES))

# Compiler settings
CC     := gcc
CFLAGS := -g -Wall
LIBS   := -lcurl -lm

# Build rules
$(EXEC): $(OBJECTS)
	$(CC) $(OBJECTS) $(CFLAGS) $(LIBS) -o $@

# Rule for building object files in build directory
$(BUILD)/%.o: $(SRC)/%.c | $(BUILD)
	$(CC) -c $(CFLAGS) $< -o $@

# Ensure build directory exists
$(BUILD):
	mkdir -p $(BUILD)

# Clean targets
clean:
	rm -f $(BUILD)/*.o

clean-all: clean
	rm -f $(EXEC)
