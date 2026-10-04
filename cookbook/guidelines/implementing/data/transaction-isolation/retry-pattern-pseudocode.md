
```
for attempt in 1..MAX:                  # MAX bounded, e.g. 4
    try:
        begin(isolation = SERIALIZABLE)
        result = run_pure_transaction()  # no external side effects
        commit()
        return result
    except SerializationFailure as e:    # SQLSTATE 40001 (or InnoDB 1213/1205)
        rollback()
        if attempt == MAX: raise
        sleep(base * 2**attempt + jitter())
```

