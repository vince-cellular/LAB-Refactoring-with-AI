# Refactoring Checklist

## Issues Found

- [x] Some functions are too large and perform multiple tasks.
- [x] Prompt text is hardcoded inside the OpenAI function.
- [x] File loading logic is repeated.
- [x] Error handling can be improved with clearer messages.
- [x] Validation and API logic are tightly coupled.
- [x] Code can be made more modular with helper functions.

## Priority

1. Improve error handling.
2. Extract helper functions.
3. Separate responsibilities into smaller functions.