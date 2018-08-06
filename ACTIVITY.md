# Record of events this morning.
There are a number of items not harvested.  I want to finish the harvesting for Rouadhan

# I find the not-harvested by running
gm search> search_response.txt

```
(gmapi-dev) mac0236:gm-api-python simon$ cat search_response.txt  | grep not | sort
083ffc19d191a1f1c70aa593e5b9f4f0   0001-01-01T00:00:00.000Z   <not harvested> ( s3://https://s3-eu-west-1.amazonaws.com/aws-c4-contextual-prod-graymeta-harvest/2018-07-10/142015/63449_001_004_001.mp4 )
2909157c0d8e37e7ec7ca0592ee67e3f   0001-01-01T00:00:00.000Z   <not harvested> ( s3://https://s3-eu-west-1.amazonaws.com/aws-c4-contextual-prod-graymeta-harvest/2018-07-10/142015/56459_001_003_005.mp4 )
2cb259beaa21dacfc3cfb442fc175e80   0001-01-01T00:00:00.000Z   <not harvested> ( s3://https://s3-eu-west-1.amazonaws.com/aws-c4-contextual-prod-graymeta-harvest/2018-07-10/142015/56459_001_002_005.mp4 )
30ce5fa9fdfe2e0097118a7e791956c4   0001-01-01T00:00:00.000Z   <not harvested> ( s3://https://s3-eu-west-1.amazonaws.com/aws-c4-contextual-prod-graymeta-harvest/2018-07-10/142015/52177_001_002_003.mp4 )
40132b0df21bb5e3d32da077c8225aab   0001-01-01T00:00:00.000Z   <not harvested> ( s3://https://s3-eu-west-1.amazonaws.com/aws-c4-contextual-prod-graymeta-harvest/2018-07-06/154036/63449_001_004_001.mp4 )
454bd7b16e897742d20989f0a4b9faea   0001-01-01T00:00:00.000Z   <not harvested> ( s3://https://s3-eu-west-1.amazonaws.com/aws-c4-contextual-prod-graymeta-harvest/2018-07-10/142015/60347_001_003_002.mp4 )
4a2d01f1d5ef53e0ccd1768b40aa0c9a   0001-01-01T00:00:00.000Z   <not harvested> ( s3://https://s3-eu-west-1.amazonaws.com/aws-c4-contextual-prod-graymeta-harvest/2018-07-05/134545/55374_001_001_001.mp4 )
4efc6a1b092ecd00c716c8725fdaecdf   0001-01-01T00:00:00.000Z   <not harvested> ( s3://https://s3-eu-west-1.amazonaws.com/aws-c4-contextual-prod-graymeta-harvest/2018-07-10/142015/52177_003_001_003.mp4 )
51147f15ea5d4131996ef1e4c9b97279   0001-01-01T00:00:00.000Z   <not harvested> ( s3://https://s3-eu-west-1.amazonaws.com/aws-c4-contextual-prod-graymeta-harvest/2018-07-05/134545/67830_005_001_001.mp4 )
552d24843d6ea4f000a037a748d5f2a7   0001-01-01T00:00:00.000Z   <not harvested> ( s3://https://s3-eu-west-1.amazonaws.com/aws-c4-contextual-prod-graymeta-harvest/2018-07-10/142015/52177_003_002_003.mp4 )
5573e061ea384dd32407e5fa1cb16cd9   0001-01-01T00:00:00.000Z   <not harvested> ( s3://https://s3-eu-west-1.amazonaws.com/aws-c4-contextual-prod-graymeta-harvest/2018-07-10/142015/55813_005_001_001.mp4 )
5e40728fe4bc674c5ba2276871b3b793   0001-01-01T00:00:00.000Z   <not harvested> ( s3://https://s3-eu-west-1.amazonaws.com/aws-c4-contextual-prod-graymeta-harvest/2018-07-06/154036/63449_001_001_001.mp4 )
6bf409636d75a795f7d10b09b3e6446b   0001-01-01T00:00:00.000Z   <not harvested> ( s3://https://s3-eu-west-1.amazonaws.com/aws-c4-contextual-prod-graymeta-harvest/2018-07-06/154036/56459_001_003_005.mp4 )
6cdd9e0df4a66a6e5ac49228d5d0bdeb   0001-01-01T00:00:00.000Z   <not harvested> ( s3://https://s3-eu-west-1.amazonaws.com/aws-c4-contextual-prod-graymeta-harvest/2018-07-10/142015/35925_001_001_002.mp4 )
a9abb4cc8e1db5c5bffd109e34e0dbe5   0001-01-01T00:00:00.000Z   <not harvested> ( s3://https://s3-eu-west-1.amazonaws.com/aws-c4-contextual-prod-graymeta-harvest/2018-07-06/154036/56459_001_001_005.mp4 )
c06435616c97b83b609df09c2da43fb3   0001-01-01T00:00:00.000Z   <not harvested> ( s3://https://s3-eu-west-1.amazonaws.com/aws-c4-contextual-prod-graymeta-harvest/2018-07-10/142015/64040_001_002_004.mp4 )
d306aeaff8f94daf6f0ca1150966f8b9   0001-01-01T00:00:00.000Z   <not harvested> ( s3://https://s3-eu-west-1.amazonaws.com/aws-c4-contextual-prod-graymeta-harvest/2018-07-06/154036/63449_001_003_001.mp4 )
dc634c5dba62b4cb30c6898540d9c6af   0001-01-01T00:00:00.000Z   <not harvested> ( s3://https://s3-eu-west-1.amazonaws.com/aws-c4-contextual-prod-graymeta-harvest/2018-07-10/142015/56459_005_002_004.mp4 )
e688e624159dc05e199e876415f12ac3   0001-01-01T00:00:00.000Z   <not harvested> ( s3://https://s3-eu-west-1.amazonaws.com/aws-c4-contextual-prod-graymeta-harvest/2018-07-10/142015/63880_001_002_001.mp4 )
fce0943ac9057c572afe606a2896a54c   0001-01-01T00:00:00.000Z   <not harvested> ( s3://https://s3-eu-west-1.amazonaws.com/aws-c4-contextual-prod-graymeta-harvest/2018-07-10/142015/35925_001_002_002.mp4 )
fe15e780541ac61d257083f542078509   0001-01-01T00:00:00.000Z   <not harvested> ( s3://https://s3-eu-west-1.amazonaws.com/aws-c4-contextual-prod-graymeta-harvest/2018-07-10/142015/56459_005_001_004.mp4 )
(gmapi-dev) mac0236:gm-api-python simon$ 
```

I harvest items individually using:

```
LOCATION_ID=083ffc19d191a1f1c70aa593e5b9f4f0
gm harvest_item 5b0fe6c3b606decb499eea7ac6971f71 $LOCATION_ID
```

I turned off Facebox as an extractor mid-flight as we don't use it.

Activity started 9.09, concluded 9.51

ITEM_ID=2909157c0d8e37e7ec7ca0592ee67e3f
gm harvest_item $ITEM_ID $LOCATION_ID





Activity

Uploaded following content

