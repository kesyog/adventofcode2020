/**
 * Approach:
 * - Store elements in a linked list for O(1) insertion/deletion
 * - Use a lookup table for O(1) searching for a node with a given value in the linked list
 * - Simulate game using described rules
 */
#include <inttypes.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

#define N_ELEMENTS 1000000
#define N_TURNS 10000000

#define ARRAY_SIZE(arr) (sizeof(arr) / sizeof(arr[0]))

typedef struct sNode_s {
  struct sNode_s *next;
  uint32_t value;
} sNode;

static sNode linked_list[N_ELEMENTS];
// Pointer at index i points to node with value i
static sNode *lookup[N_ELEMENTS + 1];

const uint32_t initial_seq[9] = {1, 6, 7, 2, 4, 8, 3, 5, 9};

static void init() {
  for (size_t i = 0; i < ARRAY_SIZE(initial_seq); ++i) {
    uint32_t val = initial_seq[i];
    linked_list[i].value = val;
    linked_list[i].next = &linked_list[i + 1];
    lookup[val] = &linked_list[i];
  }
  for (size_t i = ARRAY_SIZE(initial_seq); i < ARRAY_SIZE(linked_list); ++i) {
    uint32_t val = i + 1;
    linked_list[i].value = val;
    lookup[val] = &linked_list[i];
    if (i == ARRAY_SIZE(linked_list) - 1) {
      linked_list[i].next = &linked_list[0];
    } else {
      linked_list[i].next = &linked_list[i + 1];
    }
  }
}

int main() {
  init();

  sNode *current_node = &linked_list[0];

  for (size_t i = 0; i < N_TURNS; i++) {
    sNode *removed = current_node->next;
    sNode *last_removed = removed->next->next;
    const uint32_t removed_values[3] = {removed->value, removed->next->value,
                                        removed->next->next->value};
    current_node->next = last_removed->next;

    uint32_t dest = current_node->value - 1;
    if (dest == 0) {
      dest = ARRAY_SIZE(linked_list);
    }
    while ((dest == removed_values[0]) || (dest == removed_values[1]) ||
           (dest == removed_values[2])) {
      dest--;
      if (dest == 0) {
        dest = ARRAY_SIZE(linked_list);
      }
    }

    sNode *dest_node = lookup[dest];
    sNode *after_insertion = dest_node->next;
    dest_node->next = removed;
    last_removed->next = after_insertion;
    current_node = current_node->next;
  }
  sNode *one_node = lookup[1];
  uint64_t answer = (uint64_t)one_node->next->value * one_node->next->next->value;
  printf("%" PRIu64 "\n", answer);
}
