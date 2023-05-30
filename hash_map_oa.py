# Name: Eric Daly
# OSU Email: dalyer@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - Hashmaps
# Due Date: June 9, 2023
# Description: Hashmap using open addressing with quadratic probing to solve collisions.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the map. If key exists, update its value. Otherwise, add pair.
        :param key: Key to be added/updated.
        :param value: Value of HashEntry object
        :return: None
        """
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity*2)
        initial_index = self._hash_function(key) % self._capacity
        index = initial_index
        count = 0
        while self._buckets[index]:
            if self._buckets[index].key == key:
                self._buckets[index].value = value
                if self._buckets[index].is_tombstone is True:
                    self._buckets[index].is_tombstone = False
                    self._size += 1
                return
            elif self._buckets[index].is_tombstone is True:
                self._buckets[index] = HashEntry(key, value)
                self._size += 1
                return
            index = (initial_index + count**2) % self._capacity
            count += 1
        self._buckets[index] = HashEntry(key, value)
        self._size += 1



    def table_load(self) -> float:
        """
        Returns the table load
        :return: Float of table load.
        """
        return float(self._size/self._capacity)

    def empty_buckets(self) -> int:
        """
        Clears the contents of the hashmap, keeping the underlying capacity.
        :return: N/A
        """
        count = 0
        for i in range(self._capacity):
            if not self._buckets[i]:
                count += 1
        return count


    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the hash table. Rehashes all previous entries.
        :param new_capacity: New capacity to be used
        :return: None
        """
        # Make sure new capacity is a valid size.
        if new_capacity < self._size:
            return

        # Make sure the new capacity is a valid prime number.
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Save old Dynamic Array.
        old_da = DynamicArray()
        for i in range(self._capacity):
            old_da.append(self._buckets[i])
        # Update capacity.
        self._capacity = new_capacity

        # Create new empty DA at correct capacity.
        self._buckets = DynamicArray()
        for i in range(new_capacity):
            self._buckets.append(None)
        self._size = 0
        # Rehash all HashEntry objects from old_da
        for i in range(old_da.length()):
            if old_da[i] and old_da[i].is_tombstone is False:
                self.put(old_da[i].key, old_da[i].value)

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key.
        :param key: Key to search for.
        :return: Value or None.
        """
        initial_index = self._hash_function(key) % self._capacity
        index = initial_index
        count = 0
        while self._buckets[index]:
            if self._buckets[index].key == key and not self._buckets[index].is_tombstone:
                return self._buckets[index].value
            index = (initial_index + count**2) % self._capacity
            count += 1

    def contains_key(self, key: str) -> bool:
        """
        Boolean if key is within hash map.
        :param key: Key to be searched for.
        :return: Boolean
        """
        initial_index = self._hash_function(key) % self._capacity
        index = initial_index
        count = 0
        while self._buckets[index]:
            if self._buckets[index].key == key and not self._buckets[index].is_tombstone:
                return True
            index = (initial_index + count**2) % self._capacity
            count += 1
        return False

    def remove(self, key: str) -> None:
        """
        Removes the key and its associated value from the hash map, leaving behind a tombstone.
        :param key: Key to be removed.
        :return: None
        """
        if not self.contains_key(key):
            return

        # Quadratic Probing
        initial_index = self._hash_function(key) % self._capacity
        index = initial_index
        count = 0
        # Dont delete HashEntry, just turn it into a tombstone.
        while self._buckets[index]:
            if self._buckets[index].key == key:
                self._buckets[index].is_tombstone = True
                self._size -= 1
                return
            index = (initial_index + count**2) % self._capacity
            count += 1


    def clear(self) -> None:
        """
        Clears every index of the Dynamic Array.
        :return: None
        """
        self._size = 0
        for i in range(self._buckets.length()):
            self._buckets[i] = None

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a DA where each index contains a tuple of key/value pairs stored in the hashmap.
        :return: Dynamic Array of Tuples: (Key, Value).
        """
        # kv_da = DynamicArray()
        # elements = 0
        # flag = False
        # # Quadratic Probing starting at index 0.
        # initial_index = 0
        # index = initial_index
        # count = 0
        # while elements < self._size:
        #     # Avoid empty indexes and Tombstones.
        #     if self._buckets[index]:
        #         if self._buckets[index].is_tombstone is False:
        #             for j in range(kv_da.length()):
        #                 if kv_da[j][0] == self._buckets[index].key:
        #                     flag = True
        #             if not flag:
        #                 kv_da.append((self._buckets[index].key, self._buckets[index].value))
        #                 elements += 1
        #     flag = False
        #     index = (initial_index + count**2) % self._capacity
        #     count += 1
        #
        # return kv_da
        pass

    def __iter__(self):
        """
        TODO: Write this implementation
        """
        return self._buckets[0]

    def __next__(self):
        """
        TODO: Write this implementation
        """


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":
    #
    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(41, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(101, hash_function_1)
    # print(round(m.table_load(), 2))
    # m.put('key1', 10)
    # print(round(m.table_load(), 2))
    # m.put('key2', 20)
    # print(round(m.table_load(), 2))
    # m.put('key1', 30)
    # print(round(m.table_load(), 2))
    #
    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.get_size(), m.get_capacity())

    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(20, hash_function_1)
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    # m.resize_table(30)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(31, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    #
    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(151, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.get_size(), m.get_capacity())
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)
    #
    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(11, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))
    #
    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)

    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')
    #
    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())
    #
    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.get_size(), m.get_capacity())
    # m.resize_table(100)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())
    #
    # print("\nPDF - get_keys_and_values example 1")
    # print("------------------------")
    # m = HashMap(11, hash_function_2)
    # for i in range(1, 6):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys_and_values())
    #
    # m.resize_table(2)
    # print(m.get_keys_and_values())
    #
    # m.put('20', '200')
    # m.remove('1')
    # m.resize_table(12)
    # print(m.get_keys_and_values())

    # print("\nPDF - __iter__(), __next__() example 1")
    # print("---------------------")
    # m = HashMap(10, hash_function_1)
    # for i in range(5):
    #     m.put(str(i), str(i * 10))
    # print(m)
    # for item in m:
    #     print('K:', item.key, 'V:', item.value)
    #
    # print("\nPDF - __iter__(), __next__() example 2")
    # print("---------------------")
    # m = HashMap(10, hash_function_2)
    # for i in range(5):
    #     m.put(str(i), str(i * 24))
    # m.remove('0')
    # m.remove('4')
    # print(m)
    # for item in m:
    #     print('K:', item.key, 'V:', item.value)
