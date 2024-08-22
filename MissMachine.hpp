#pragma once
#include<cstdint>
#include<vector>
#include<algorithm>
#include<cassert>
struct MissingLink {
	struct MissingLink* next;  // I know that pointers are 8 bytes on this machine.
	uint64_t data;             
	MissingLink(): next(NULL) {}
};

extern "C"
struct MissingLink * do_load_misses(struct MissingLink * start, uint64_t count) {
	for(uint64_t i = 0; i < count; i++) { // Here's the loop that does this misses. It's very simple.
		start = start->next;
	}
	return start;
}

extern "C"
struct MissingLink * do_store_misses(struct MissingLink * start, uint64_t count) {
	for(uint64_t i = 0; i < count; i++) { // Here's the loop that does this misses. It's very simple.
		start = start->next;
		start->data = i;
	}
	return start;
}

class MissMachine {
public:
	size_t link_count;
	size_t link_bytes;
	uint8_t *data;
	MissingLink * dummy; // this is here to prevent the compiler from optimizing out the  calls to do_load_misses()
	std::vector<MissingLink*> links;
    
	MissMachine(size_t link_bytes, size_t total_bytes): link_count(total_bytes/link_bytes), link_bytes(link_bytes) {
		assert(total_bytes > link_bytes);
		assert(link_bytes >= sizeof(void*));
		data = new uint8_t[link_bytes * link_count];
		for(unsigned int i = 0; i < link_count; i++) {
			links.push_back(new (reinterpret_cast<MissingLink*>(reinterpret_cast<uintptr_t>(data) + i * link_bytes)) MissingLink);
		}
	}
    
	void make_links() {
		for(unsigned int i = 0; i < link_count -1; i++) {
			links[i]->next = links[i + 1];
		}
		links[link_count -1]->next = links[0];
	}
    
	inline MissingLink * load_miss(size_t count, size_t start = 0) {
		return dummy = do_load_misses(links[start], count);
	}
    
	inline MissingLink * store_miss(size_t count, size_t start = 0) {
		assert(link_bytes >= sizeof(MissingLink));
		return dummy = do_store_misses(links[start], count);
	}
    
	void shuffle(uint64_t seed =0xDEADBEEF) {
		std::random_shuffle(links.begin(), links.end());
	}

	~MissMachine() {
		delete [] data;
	}
};
