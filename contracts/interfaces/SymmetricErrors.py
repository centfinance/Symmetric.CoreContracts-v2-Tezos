# Math
ADD_OVERFLOW = 0
SUB_OVERFLOW = 1
SUB_UNDERFLOW = 2
MUL_OVERFLOW = 3
ZERO_DIVISION = 4
DIV_INTERNAL = 5
X_OUT_OF_BOUNDS = 6
Y_OUT_OF_BOUNDS = 7
PRODUCT_OUT_OF_BOUNDS = 8
INVALID_EXPONENT = 9

# Input
OUT_OF_BOUNDS = 100
UNSORTED_ARRAY = 101
UNSORTED_TOKENS = 102
INPUT_LENGTH_MISMATCH = 103
ZERO_TOKEN = 104
INSUFFICIENT_DATA = 105

# Shared pools
MIN_TOKENS = 200
MAX_TOKENS = 201
MAX_SWAP_FEE_PERCENTAGE = 202
MIN_SWAP_FEE_PERCENTAGE = 203
MINIMUM_SPT = 204
CALLER_NOT_VAULT = 205
UNINITIALIZED = 206
SPT_IN_MAX_AMOUNT = 207
SPT_OUT_MIN_AMOUNT = 208
EXPIRED_PERMIT = 209
NOT_TWO_TOKENS = 210
DISABLED = 211

# Pools
MIN_AMP = 300
MAX_AMP = 301
MIN_WEIGHT = 302
MAX_STABLE_TOKENS = 303
MAX_IN_RATIO = 304
MAX_OUT_RATIO = 305
MIN_SPT_IN_FOR_TOKEN_OUT = 306
MAX_OUT_SPT_FOR_TOKEN_IN = 307
NORMALIZED_WEIGHT_INVARIANT = 308
INVALID_TOKEN = 309
UNHANDLED_JOIN_KIND = 310
ZERO_INVARIANT = 311
ORACLE_INVALID_SECONDS_QUERY = 312
ORACLE_NOT_INITIALIZED = 313
ORACLE_QUERY_TOO_OLD = 314
ORACLE_INVALID_INDEX = 315
ORACLE_BAD_SECS = 316
AMP_END_TIME_TOO_CLOSE = 317
AMP_ONGOING_UPDATE = 318
AMP_RATE_TOO_HIGH = 319
AMP_NO_ONGOING_UPDATE = 320
STABLE_INVARIANT_DIDNT_CONVERGE = 321
STABLE_GET_BALANCE_DIDNT_CONVERGE = 322
RELAYER_NOT_CONTRACT = 323
BASE_POOL_RELAYER_NOT_CALLED = 324
REBALANCING_RELAYER_REENTERED = 325
GRADUAL_UPDATE_TIME_TRAVEL = 326
SWAPS_DISABLED = 327
CALLER_IS_NOT_LBP_OWNER = 328
PRICE_RATE_OVERFLOW = 329
INVALID_JOIN_EXIT_KIND_WHILE_SWAPS_DISABLED = 330
WEIGHT_CHANGE_TOO_FAST = 331
LOWER_GREATER_THAN_UPPER_TARGET = 332
UPPER_TARGET_TOO_HIGH = 333
UNHANDLED_BY_LINEAR_POOL = 334
OUT_OF_TARGET_RANGE = 335
UNHANDLED_EXIT_KIND = 336
UNAUTHORIZED_EXIT = 337
MAX_MANAGEMENT_SWAP_FEE_PERCENTAGE = 338
UNHANDLED_BY_MANAGED_POOL = 339
UNHANDLED_BY_PHANTOM_POOL = 340
TOKEN_DOES_NOT_HAVE_RATE_PROVIDER = 341
INVALID_INITIALIZATION = 342
OUT_OF_NEW_TARGET_RANGE = 343
FEATURE_DISABLED = 344
UNINITIALIZED_POOL_CONTROLLER = 345
SET_SWAP_FEE_DURING_FEE_CHANGE = 346
SET_SWAP_FEE_PENDING_FEE_CHANGE = 347
CHANGE_TOKENS_DURING_WEIGHT_CHANGE = 348
CHANGE_TOKENS_PENDING_WEIGHT_CHANGE = 349
MAX_WEIGHT = 350
UNAUTHORIZED_JOIN = 351
MAX_MANAGEMENT_AUM_FEE_PERCENTAGE = 352
FRACTIONAL_TARGET = 353
ADD_OR_REMOVE_SPT = 354
INVALID_CIRCUIT_BREAKER_BOUNDS = 355
CIRCUIT_BREAKER_TRIPPED = 356
MALICIOUS_QUERY_REVERT = 357
JOINS_EXITS_DISABLED = 358

# Lib
REENTRANCY = 400
SENDER_NOT_ALLOWED = 401
PAUSED = 402
PAUSE_WINDOW_EXPIRED = 403
MAX_PAUSE_WINDOW_DURATION = 404
MAX_BUFFER_PERIOD_DURATION = 405
INSUFFICIENT_BALANCE = 406
INSUFFICIENT_ALLOWANCE = 407
ERC20_TRANSFER_FROM_ZERO_ADDRESS = 408
ERC20_TRANSFER_TO_ZERO_ADDRESS = 409
ERC20_MINT_TO_ZERO_ADDRESS = 410
ERC20_BURN_FROM_ZERO_ADDRESS = 411
ERC20_APPROVE_FROM_ZERO_ADDRESS = 412
ERC20_APPROVE_TO_ZERO_ADDRESS = 413
ERC20_TRANSFER_EXCEEDS_ALLOWANCE = 414
ERC20_DECREASED_ALLOWANCE_BELOW_ZERO = 415
ERC20_TRANSFER_EXCEEDS_BALANCE = 416
ERC20_BURN_EXCEEDS_ALLOWANCE = 417
SAFE_ERC20_CALL_FAILED = 418
ADDRESS_INSUFFICIENT_BALANCE = 419
ADDRESS_CANNOT_SEND_VALUE = 420
SAFE_CAST_VALUE_CANT_FIT_INT256 = 421
GRANT_SENDER_NOT_ADMIN = 422
REVOKE_SENDER_NOT_ADMIN = 423
RENOUNCE_SENDER_NOT_ALLOWED = 424
BUFFER_PERIOD_EXPIRED = 425
CALLER_IS_NOT_OWNER = 426
NEW_OWNER_IS_ZERO = 427
CODE_DEPLOYMENT_FAILED = 428
CALL_TO_NON_CONTRACT = 429
LOW_LEVEL_CALL_FAILED = 430
NOT_PAUSED = 431
ADDRESS_ALREADY_ALLOWLISTED = 432
ADDRESS_NOT_ALLOWLISTED = 433
ERC20_BURN_EXCEEDS_BALANCE = 434
INVALID_OPERATION = 435
CODEC_OVERFLOW = 436
IN_RECOVERY_MODE = 437
NOT_IN_RECOVERY_MODE = 438
INDUCED_FAILURE = 439
EXPIRED_SIGNATURE = 440
MALFORMED_SIGNATURE = 441
SAFE_CAST_VALUE_CANT_FIT_UINT64 = 442
UNHANDLED_FEE_TYPE = 443
BURN_FROM_ZERO = 444

# Vault
INVALID_POOL_ID = 500
CALLER_NOT_POOL = 501
SENDER_NOT_ASSET_MANAGER = 502
USER_DOESNT_ALLOW_RELAYER = 503
INVALID_SIGNATURE = 504
EXIT_BELOW_MIN = 505
JOIN_ABOVE_MAX = 506
SWAP_LIMIT = 507
SWAP_DEADLINE = 508
CANNOT_SWAP_SAME_TOKEN = 509
UNKNOWN_AMOUNT_IN_FIRST_SWAP = 510
MALCONSTRUCTED_MULTIHOP_SWAP = 511
INTERNAL_BALANCE_OVERFLOW = 512
INSUFFICIENT_INTERNAL_BALANCE = 513
INVALID_ETH_INTERNAL_BALANCE = 514
INVALID_POST_LOAN_BALANCE = 515
INSUFFICIENT_ETH = 516
UNALLOCATED_ETH = 517
ETH_TRANSFER = 518
CANNOT_USE_ETH_SENTINEL = 519
TOKENS_MISMATCH = 520
TOKEN_NOT_REGISTERED = 521
TOKEN_ALREADY_REGISTERED = 522
TOKENS_ALREADY_SET = 523
TOKENS_LENGTH_MUST_BE_2 = 524
NONZERO_TOKEN_BALANCE = 525
BALANCE_TOTAL_OVERFLOW = 526
POOL_NO_TOKENS = 527
INSUFFICIENT_FLASH_LOAN_BALANCE = 528

# Fees
SWAP_FEE_PERCENTAGE_TOO_HIGH = 600
FLASH_LOAN_FEE_PERCENTAGE_TOO_HIGH = 601
INSUFFICIENT_FLASH_LOAN_FEE_AMOUNT = 602
AUM_FEE_PERCENTAGE_TOO_HIGH = 603

# FeeSplitter
SPLITTER_FEE_PERCENTAGE_TOO_HIGH = 700

# Misc
UNIMPLEMENTED = 998
SHOULD_NOT_HAPPEN = 999

# Views
CALC_OUT_GIVEN_IN_INVALID = 800
CALC_IN_GIVEN_OUT_INVALID = 801
CALCULATE_INVARIANT_INVALID = 802
CALC_SPT_OUT_GIVEN_EXACT_TOKENS_IN_INVALID = 803
CALC_SPT_IN_GIVEN_EXACT_TOKENS_OUT_INVALID = 804
CALC_TOKEN_IN_GIVEN_EXACT_SPT_OUT_INVALID = 805
CALC_TOKEN_OUT_GIVEN_EXACT_SPT_IN_INVALID = 806

GET_PRE_JOIN_EXIT_PROTOCOL_FEES_INVALID = 807
GET_POST_JOIN_EXIT_PROTOCOL_FEES_INVALID = 808
GET_RATE_PRODUCT_INVALID = 809

BEFORE_JOIN_POOL_INVALID = 810
BEFORE_EXIT_POOL_INVALID = 811

ON_SWAP_INVALID = 812

GET_POOL_TOKENS_INVALID = 813

GET_NEXT_POOL_NONCE_INVALID = 814

GET_RATE_INVALID = 815

GET_SWAP_FEE_PERCEMTAGE_INVALID = 816
GET_YIELD_FEE_PERCEMTAGE_INVALID = 817