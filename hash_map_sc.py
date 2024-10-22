# Name: Eric Daly
# OSU Email: dalyer@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - Hashmaps
# Due Date: June 9, 2023
# Description: Hashmap using chaining to solve collisions.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Updates the key/value pair in the hash map. If key already exists, associated value will be replaced.
        If key is not in map, new pair will be added.
        :param key: Key to be updated.
        :param value: Value to be updated to associate with key.
        :return: None
        """
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        # Determine index and check if key already exists.
        index = self._hash_function(key) % self._capacity
        if self._buckets[index].contains(key) is None:
            self._buckets[index].insert(key, value)
            self._size += 1
        # If key exists in bucket, replace its value.
        elif self._buckets[index].contains(key):
            for node in self._buckets[index]:
                if node.key == key:
                    node.value = value

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        :return: Number of empty buckets
        """
        count = 0
        for i in range(0, self._capacity):
            if self._buckets[i].length() == 0:
                count += 1
        return count

    def table_load(self) -> float:
        """
        Returns the table load
        :return: Float of table load.
        """
        elements = 0
        for i in range(self._capacity):
            elements += self._buckets[i].length()

        return float(elements/self._capacity)


    def clear(self) -> None:
        """
        Clears the contents of the hashmap, keeping the underlying capacity.
        :return: N/A
        """
        for i in range(self._buckets.length()):
            self._buckets.set_at_index(i, LinkedList())
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash table to the new capacity, or the next prime number after it.
        :param new_capacity: New capacity
        :return:
        """
        # Save old hashmap for rehashing linked list nodes.
        old_da = self._buckets
        # Make sure new capacity is valid and prime.
        if new_capacity < 1:
            return
        elif not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Create new underlying DA with empty LinkedLists.
        self._capacity = new_capacity
        self._buckets = DynamicArray()
        for i in range(0, new_capacity):
            self._buckets.append(LinkedList())
        self._size = 0

        # Look for active linked lists and iterate through them, rehashing their key/value pairs.
        for index in range(old_da.length()):
            if old_da.length() > 0:
                for node in old_da[index]:
                    self.put(node.key, node.value)

    def get(self, key: str):
        """
        Returns the value associated with the given key.
        :param key: Key to be searched for.
        :return: Value or None.
        """
        index = self._hash_function(key) % self._capacity
        if self._buckets[index].contains(key) is None:
            return
        # If key exists in bucket, find its value
        elif self._buckets[index].contains(key):
            for node in self._buckets[index]:
                if node.key == key:
                    return node.value

    def contains_key(self, key: str) -> bool:
        """
        Returns boolean if key is or isnt in has map.
        :param key: Key to be searched for.
        :return: True if found, False otherwise.
        """
        index = self._hash_function(key) % self._capacity
        if self._buckets[index].contains(key):
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key/value pair from the hashmap.
        :param key: Key of pair to be removed
        :return: None
        """
        if not self.contains_key(key):
            return
        else:
            index = self._hash_function(key) % self._capacity
            self._buckets[index].remove(key)
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash map.
        :return: DynamicArray
        """
        kv_da = DynamicArray()
        for i in range(0, self._capacity):
            if self._buckets[i].length() > 0:
                for node in self._buckets[i]:
                    kv_da.append((node.key, node.value))
        return kv_da


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Returns a tuple containing a DA comprised of the mode value(s) and the frequency.
    :param da: DynamicArray to be searched.
    :return: Tuple: (DynamicArray of values, frequency of values)
    """
    map = HashMap()
    mode_da = DynamicArray()
    mode_freq = 0
    # Hash all the values in the DA.
    for i in range(da.length()):
        if not map.contains_key(da[i]):
            map.put(da[i], 0)
        # Get current frequency of that key and increase it by 1.
        freq = map.get(da[i])
        freq += 1
        map.put(da[i], freq)

    kv_da = map.get_keys_and_values()
    # Create DA for the modes.
    for i in range(kv_da.length()):
        if kv_da[i][1] > mode_freq:
            mode_da = DynamicArray()
            mode_da.append(kv_da[i][0])
            mode_freq = kv_da[i][1]
        elif kv_da[i][1] == mode_freq:
            mode_da.append(kv_da[i][0])



    return (mode_da, mode_freq)


    # Iterate through the hashmap



# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
