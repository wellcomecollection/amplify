import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { WorldcatResultsComponent } from './worldcat-results.component';

describe('WorldcatResultsComponent', () => {
  let component: WorldcatResultsComponent;
  let fixture: ComponentFixture<WorldcatResultsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ WorldcatResultsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(WorldcatResultsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
