import { TestBed } from '@angular/core/testing';

import { UrlCheckService } from './url-check-service';

describe('UrlCheckService', () => {
  let service: UrlCheckService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(UrlCheckService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
