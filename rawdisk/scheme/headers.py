# -*- coding: utf-8 -*-
from ctypes import Structure, c_ushort, c_ubyte, c_uint, c_ulonglong, \
    c_byte, c_char, c_wchar


class MBR_PARTITION_ENTRY(Structure):
    """Represents MBR partition entry

    Attributes:
        boot_indicator (ubyte): Boot indicator bit flag: 0 = no, 0x80 = \
        bootable (or "active")
        starting_head (ubyte): Starting head for the partition
        starting_sector (6 bits): Starting sector for the partition
        starting_cylinder (10 bits): Starting cylinder for the partition
        part_type (ubyte): Partition type id
        ending_head (ubyte): Ending head of the partition
        ending_sector (6 bits): Ending sector
        ending_cylinder (10 bits): Ending cylinder
        relative_sector (uint): The offset from the beginning of the disk to \
        the beginning of the volume, counting by sectors.
        total_sectors (uint): The total number of sectors in the volume.
        part_offset (uint): The offset from the beginning of the disk \
        to the beginning of the volume, counting by bytes.

    See Also:
        | MBR Table (http://technet.microsoft.com/en-us/library/cc976786.aspx)
        | MBR Partition Types \
        (http://en.wikipedia.org/wiki/Partition_type#List_of_partition_IDs)
    """
    _fields_ = [
        ("boot_indicator",      c_ubyte),
        ("starting_head",       c_ubyte),
        ("starting_sector",     c_ubyte),
        ("starting_cylinder",   c_ubyte),
        ("part_type",           c_ubyte),
        ("ending_head",         c_ubyte),
        ("ending_sector",       c_ubyte),
        ("ending_cylinder",     c_ubyte),
        ("relative_sector",     c_ubyte),
        ("total_sectors",       c_uint),
        ("part_offset",         c_uint),
    ]


class GPT_HEADER(Structure):
    """Represents GUID partition table header (LBA1).

    Attributes:
        signature (str): "EFI PART", 45h 46h 49h 20h 50h 41h 52h 54h
        revision (uint): GPT Revision
        header_size (uint): Total length of gpt header
        crc32 (uint): CRC32 of the header
        current_lba (ulonglong): LBA location of this header
        backup_lba (ulonglong): LBA loction of header's copy
        first_usable_lba (ulonglong): First usable LBA for partitions
        last_usable_lba (ulonglong): Last usable LBA for partitions
        disk_guid (char[16]): Disk GUID (UUID for Unixes)
        part_lba (ulonglong): Starting LBA of array of partition entries
        num_partitions (uint): Number of partition entries in array
        part_size (uint): Size of a single partition entry (usually 128)
        part_array_crc32 (uint): CRC32 of partition array

    Raises:
        Exception: If signature does not match valid GPT signature

    See Also:
        http://en.wikipedia.org/wiki/GUID_Partition_Table#Partition_table_header_.28LBA_1.29
    """
    _fields_ = [
        ("signature",           c_char * 8),
        ("revision",            c_uint),
        ("header_size",         c_uint),
        ("crc32",               c_uint),
        ("current_lba",         c_ulonglong),
        ("backup_lba",          c_ulonglong),
        ("first_usable_lba",    c_ulonglong),
        ("last_usable_lba",     c_ulonglong),
        ("disk_guid",           c_char * 36),
        ("part_lba",            c_ulonglong),
        ("num_partitions",      c_uint),
        ("part_size",           c_uint),
        ("part_array_crc32",    c_uint),
    ]
